import torch
import torch.nn.parallel
from torch.utils.data import Dataset, DataLoader
import torchvision

import pandas as pd
import numpy as np
from PIL import Image
import os
import argparse

from models import modules, net, resnet, densenet, senet
from transforms import ToTensor, Normalize


class depthDataset(Dataset):
    '''
        Our super-simple data loader, an implementation of an torch.utils.data.DataLoader object
    '''

    def __init__(self, csv_file, transform=None):

        self.frame = pd.read_csv(csv_file, header=None)
        self.transform = transform

    def __getitem__(self, idx):

        image_name = self.frame.loc[idx, 0]
        output_name = self.frame.loc[idx, 1]

        _, image_extension = os.path.splitext(image_name)

        # If the extension of file is .npy we treat is as a numpy array
        # Otherwise, we treat is an image, and Pillow will take care of it.

        if image_extension == '.npy':
            image = np.load(image_name)
        else:
            image = Image.open(image_name)

        sample = {'image': image, 'output_name': output_name}

        if self.transform:
            sample = self.transform(sample)

        return sample

    def __len__(self):
        return len(self.frame)


def get_evaluation_data(batch_size=1, csv_file=''):
    '''
        Loads the evaluation data from a CSV file

        Input parameters: batch_size, the number of samples in a batch
                          csv_file, a file containing the input data

        Return type: a torch.utils.data.DataLoader object
    '''

    imagenet_stats = {'mean': [0.485, 0.456, 0.406],
                      'std': [0.229, 0.224, 0.225]}

    # A transform is applied to the input data, converting it
    # to tensor format and normalizing it to have the same mean
    # and standard deviation of the ImageNet dataset
    #
    # This is related to the fact the SENet 'backbone' is indeed
    # trained on the ImageNet dataset, but I am not sure I fully
    # understand this.

    my_transform = torchvision.transforms.Compose([
                                           ToTensor(),
                                           Normalize(imagenet_stats['mean'],
                                                     imagenet_stats['std'])
                                       ])

    transformed_testing = depthDataset(csv_file=csv_file,
                                       transform=my_transform)

    # One should check carefully num_workers and pin_memory,
    # which could be important once we use CUDA.

    dataloader_testing = DataLoader(transformed_testing, batch_size,
                                    shuffle=False, num_workers=0, pin_memory=False)

    return dataloader_testing


def define_model(is_resnet, is_densenet, is_senet):
    '''
        Selects a model to use.

        A pretrained CNN (ResNet, DenseNet or SENet) is
        used for transfer learning, and is 'encoded' to form our final model.

        Note: we only worked with SENet so far, other models are completely
        untested.
    '''

    if is_resnet:
        original_model = resnet.resnet50(pretrained = True)
        Encoder = modules.E_resnet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])

    if is_densenet:
        original_model = densenet.densenet161(pretrained=True)
        Encoder = modules.E_densenet(original_model)
        model = net.model(Encoder, num_features=2208, block_channel = [192, 384, 1056, 2208])

    if is_senet:
        original_model = senet.senet154(pretrained=None)
        Encoder = modules.E_senet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])

    return model


def eval_main(csv_filename, model_filename):
    '''
        The main function.

        Loads the dataset, the pre-trained networks and
        evaluates it over the input data.

        Parameters: csv_filename, a string with the path of the CSV file
                    model_filename, a string with the location of the pretrained model
    '''
    #only if run on GPU SERVER!!!!
    os.environ['CUDA_VISIBLE_DEVICES'] = ''

    if(os.path.isfile(csv_filename) == False):
        print('The specified CSV file ({}) does not exist. Quitting.'.format(csv_filename))
        return

    if(os.path.isfile(model_filename) == False):
        print('The specified model file ({}) does not exist. Quitting.'.format(model_filename))
        return

    # Input images can be loaded in batches, resulting in a tensor of shape
    # [ nr_batches, nr_channels, x_dim, y_dim ]
    #
    # Batches do not make a big difference when running on CPU, but they
    # speed up the process a lot when running on GPU/CUDA.

    batch_size = 1
    test_loader = get_evaluation_data(batch_size, csv_filename)

    for i, sample_batched in enumerate(test_loader):

        image = sample_batched['image']
        print('Loaded i = {}, input shape = {}'.format(i,image.shape))

    # Now we can defined the model to be used for evaluation

    model = define_model(is_resnet=False, is_densenet=False, is_senet=True)
    model = torch.nn.DataParallel(model,device_ids=[0,1])

    # The pre-trained weights of the model are loaded in a dictionary

    state_dict = torch.load(model_filename,map_location=torch.device('cpu'))['state_dict']

    # The pre-trained weights are in slightly different format, so that we need to convert their names.

    new_state_dict = state_dict.copy()

    for key, value in state_dict.items():
        new_state_dict['module.' + key] = new_state_dict.pop(key)

    # The following checks are for compatibility with both the pre-trained weights and the new ones

    if 'module.E.Harm.dct' in new_state_dict:
        new_state_dict.pop('module.E.Harm.dct')

    if 'module.E.Harm.weight' in new_state_dict:
        new_state_dict.pop('module.E.Harm.weight')

    if 'module.E.Harm.bias' in new_state_dict:
        new_state_dict.pop('module.E.Harm.bias')

    model.load_state_dict(new_state_dict)

    # We are ready to set the model in 'evaluation' mode...

    model.eval()

    # ...and go through all the test images

    for i, sample_batched in enumerate(test_loader):

        image = sample_batched['image']

        print('Input #{}, shape is {}'.format(i,image.shape))

        # The model is evaluated on the input data, and the output heightmap
        # is upsampled from 250x250 to 500x500, to match the input data

        output = model(image)
        output = torch.nn.functional.interpolate(output, size=(500,500), mode='bilinear')

        print('Output #{}, shape (after resampling) is {}'.format(i,output.shape))

        # The output is saved in numpy format
        # FIXME: this works only on the first element of a batch, so we need to work with a batch size of 1

        np.save(sample_batched['output_name'][0], output.detach().numpy()[0,0], allow_pickle=False)


if __name__ == '__main__':

    # At first, we construct a command line parser...

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--csv', default='')
    parser.add_argument('--model', default='')

    # ...end we actually use it to parse the command line

    args = parser.parse_args()

    eval_main(args.csv, args.model)
