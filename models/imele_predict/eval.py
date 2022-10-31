import torch
import torch.nn.parallel
from torch.utils.data import Dataset, DataLoader

import torchvision
#from torchvision import transforms, utils

import pandas as pd
import numpy as np
import cv2
from PIL import Image

from models import modules, net, resnet, densenet, senet
from transforms import ToTensor, Normalize


class depthDataset(Dataset):

    def __init__(self, csv_file, transform=None):

        self.frame = pd.read_csv(csv_file, header=None)
        self.transform = transform


    def __getitem__(self, idx):

        image_name = self.frame.loc[idx, 0]
        image = Image.open(image_name)

        sample = {'image': image}

        if self.transform:
            sample = self.transform(sample)

        return sample


    def __len__(self):
        return len(self.frame)


def get_evaluation_data(batch_size=16, csv_file=''):

    imagenet_stats = {'mean': [0.485, 0.456, 0.406],
                      'std': [0.229, 0.224, 0.225]}

    my_transform = torchvision.transforms.Compose([
                                           ToTensor(),
                                           Normalize(imagenet_stats['mean'],
                                                     imagenet_stats['std'])
                                       ])

    transformed_testing = depthDataset(csv_file=csv_file,
                                       transform=my_transform)

    dataloader_testing = DataLoader(transformed_testing, batch_size,
                                    shuffle=False, num_workers=0, pin_memory=False)

    return dataloader_testing


def define_model(is_resnet, is_densenet, is_senet):

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


def eval_main():

    csv_filename='test0.csv'
    model_filename=' ../../data/external/Block0_skip_model_110.pth.tar'

    batch_size = 1
    test_loader = get_evaluation_data(batch_size, csv_filename)

    for i, sample_batched in enumerate(test_loader):

        image = sample_batched['image']
        print('Loader i={}: input shape {}'.format(i,image.shape))


    model = define_model(is_resnet=False, is_densenet=False, is_senet=True)
    model = torch.nn.DataParallel(model,device_ids=[0,1])
    state_dict = torch.load(model_filename,map_location=torch.device('cpu'))['state_dict']

    # The pre-trained weights are in slightly different format, so that we need to convert their names.


    new_state_dict = state_dict.copy()

    for key, value in state_dict.items():
        new_state_dict['module.' + key] = new_state_dict.pop(key)

    new_state_dict.pop('module.E.Harm.dct')
    new_state_dict.pop('module.E.Harm.weight')
    new_state_dict.pop('module.E.Harm.bias')

    model.load_state_dict(new_state_dict)

    # We are ready to set the model in 'evaluation' mode...

    model.eval()

    # ...and go through all the test images

    for i, sample_batched in enumerate(test_loader):

        image = sample_batched['image']

        print('Input #{}, shape is {}'.format(i,image.shape))

        output = model(image)
        output = torch.nn.functional.interpolate(output, size=(500,500), mode='bilinear')

        print('Output #{}, shape (after resampling) is {}'.format(i,output.shape))

        img1 = output[0]
        #save_image(img1, 'img{}.png'.format(i))

        np.save('img{}.in.npy'.format(i), image.detach().numpy()[0,0], allow_pickle=False)
        np.save('img{}.out.npy'.format(i), output.detach().numpy()[0,0], allow_pickle=False)


if __name__ == '__main__':
    eval_main()
