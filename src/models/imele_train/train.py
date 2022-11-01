import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
from torch.utils.data import Dataset, DataLoader
import torchvision

from PIL import Image
import cv2

import os
import sys
import time
import argparse

from models import modules, net, resnet, densenet, senet
import sobel
from transforms import *

class depthDataset(Dataset):

    def __init__(self, csv_file, transform=None):
        self.frame = pd.read_csv(csv_file, header=None)
        self.transform = transform

    def __getitem__(self, idx):

        image_name = self.frame.loc[idx, 0]
        depth_name = self.frame.loc[idx, 1]

        image = Image.open(image_name)

        depth = cv2.imread(depth_name, -1)
        depth = (depth*1000).astype(np.uint16)
        depth = Image.fromarray(depth)

        sample = {'image': image, 'depth': depth}

        if self.transform:
            sample = self.transform(sample)

        return sample

    def __len__(self):
        return len(self.frame)


def get_training_data(batch_size=64, csv_data=''):

    __imagenet_stats = {'mean': [0.485, 0.456, 0.406],
                        'std': [0.229, 0.224, 0.225]}

    csv = csv_data

    my_transforms = torchvision.transforms.Compose([
                                                        ToTensor(),
                                                        Normalize(__imagenet_stats['mean'],
                                                                  __imagenet_stats['std'])
                                                   ])

    transformed_training_trans = depthDataset(csv_file=csv,
                                              transform=my_transforms)

    dataloader_training = DataLoader(transformed_training_trans, batch_size, num_workers=4, pin_memory=False)

    return dataloader_training


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
        original_model = senet.senet154(pretrained='imagenet')
        Encoder = modules.E_senet(original_model)
        model = net.model(Encoder, num_features=2048, block_channel = [256, 512, 1024, 2048])

    return model


def train_main(use_cuda):

    global args
    args = parser.parse_args()
    model = define_model(is_resnet=False, is_densenet=False, is_senet=True)

    if args.start_epoch != 0:

        if use_cuda == True:
            model = torch.nn.DataParallel(model, device_ids=[0, 1]).cuda()
            model = model.cuda()
        else:
            model = torch.nn.DataParallel(model, device_ids=[0, 1])

        state_dict = torch.load(args.model)['state_dict']
        model.load_state_dict(state_dict)
        batch_size = 2
    else:
        if use_cuda == True:
            model = model.cuda()

        batch_size = 2

    cudnn.benchmark = True
    optimizer = torch.optim.Adam(model.parameters(), args.lr, weight_decay=args.weight_decay)

    train_loader = get_training_data(batch_size, args.csv)

    for epoch in range(args.start_epoch, args.epochs):

        adjust_learning_rate(optimizer, epoch)
        train(train_loader, model, optimizer, epoch, use_cuda)

        out_name = save_model+str(epoch)+'.pth.tar'
        modelname = save_checkpoint({'state_dict': model.state_dict()},out_name)
        print(modelname)



def train(train_loader, model, optimizer, epoch, use_cuda):

    criterion = nn.L1Loss()
    batch_time = AverageMeter()
    losses = AverageMeter()

    # The model is set to training mode

    model.train()

    cos = nn.CosineSimilarity(dim=1, eps=0)

    if use_cuda ==  True:
        get_gradient = sobel.Sobel().cuda()
    else:
        get_gradient = sobel.Sobel()

    global args
    args = parser.parse_args()

    end = time.time()
    for i, sample_batched in enumerate(train_loader):

        image, depth = sample_batched['image'], sample_batched['depth']

        # Not sure this resizing should go here, but it does the trick!
        depth = torch.nn.functional.interpolate(depth, size=(250,250), mode='bilinear')

        if use_cuda == True:
            depth = depth.cuda(non_blocking=True)
            image = image.cuda()

        image = torch.autograd.Variable(image)
        depth = torch.autograd.Variable(depth)

        ones = torch.ones(depth.size(0), 1, depth.size(2),depth.size(3)).float()

        if use_cuda == True:
            ones = ones.cuda()

        ones = torch.autograd.Variable(ones)
        optimizer.zero_grad()

        output = model(image)

        #if i%200 == 0:
            #x = output[0]
            #x = x.view([220,220])
            #x = x.cpu().detach().numpy()
            #x = x*100000
            #x2 = depth[0]
            #print(x)
            #x2 = x2.view([220,220])
            #x2 = x2.cpu().detach().numpy()
            #x2 = x2  *100000
            #print(x2)

            #x = x.astype('uint16')
            #cv2.imwrite(args.data+str(i)+'_out.png',x)
            #x2 = x2.astype('uint16')
            #cv2.imwrite(args.data+str(i)+'_out2.png',x2)


        depth_grad = get_gradient(depth)
        output_grad = get_gradient(output)
        depth_grad_dx = depth_grad[:, 0, :, :].contiguous().view_as(depth)
        depth_grad_dy = depth_grad[:, 1, :, :].contiguous().view_as(depth)
        output_grad_dx = output_grad[:, 0, :, :].contiguous().view_as(depth)
        output_grad_dy = output_grad[:, 1, :, :].contiguous().view_as(depth)
        depth_normal = torch.cat((-depth_grad_dx, -depth_grad_dy, ones), 1)
        output_normal = torch.cat((-output_grad_dx, -output_grad_dy, ones), 1)
        loss_depth = torch.log(torch.abs(output - depth) + 0.5).mean()
        loss_dx = torch.log(torch.abs(output_grad_dx - depth_grad_dx) + 0.5).mean()
        loss_dy = torch.log(torch.abs(output_grad_dy - depth_grad_dy) + 0.5).mean()
        loss_normal = torch.abs(1 - cos(output_normal, depth_normal)).mean()
        loss = loss_depth + loss_normal + (loss_dx + loss_dy)
        losses.update(loss.data, image.size(0))
        loss.backward()
        optimizer.step()

        batch_time.update(time.time() - end)
        end = time.time()

        batchSize = depth.size(0)

        print('Epoch: [{0}][{1}/{2}]\t'
              'Time {batch_time.val:.3f} ({batch_time.sum:.3f})\t'
              'Loss {loss.val:.4f} ({loss.avg:.4f})'
              .format(epoch, i, len(train_loader), batch_time=batch_time, loss=losses))


def adjust_learning_rate(optimizer, epoch):
    lr = args.lr * (0.9 ** (epoch // 5))

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class AverageMeter(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def save_checkpoint(state, filename='test.pth.tar'):
    torch.save(state, filename)
    return filename

if __name__ == '__main__':

    global parser
    parser = argparse.ArgumentParser(description='PyTorch DenseNet Training')
    parser.add_argument('--epochs', default=100, type=int, help='number of total epochs to run')
    parser.add_argument('--start_epoch', default=0, type=int, help='manual epoch number (useful on restarts)')
    parser.add_argument('--lr', '--learning-rate', default=0.0001, type=float, help='initial learning rate')
    parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
    parser.add_argument('--weight-decay', '--wd', default=1e-4, type=float, help='weight decay (default: 1e-4)')

    parser.add_argument('--data', default='adjust')
    parser.add_argument('--csv', default='')
    parser.add_argument('--model', default='')

    args = parser.parse_args()
    save_model = args.data + '/' + args.data + '_model_'
    if not os.path.exists(args.data):
        os.makedirs(args.data)

    train_main(torch.cuda.is_available())
