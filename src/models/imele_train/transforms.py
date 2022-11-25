import torch
import numpy as np

class ToTensor(object):
    """Convert a ``PIL.Image`` or ``numpy.ndarray`` to tensor.
    Converts a PIL.Image or numpy.ndarray (H x W x C) in the range
    [0, 255] to a torch.FloatTensor of shape (C x H x W) in the range [0.0, 1.0].
    """
    def __init__(self,is_train=True):
        self.is_train = is_train

    def __call__(self, sample):
        image, depth, vhm = sample['image'], sample['depth'], sample['vhm']
        """
            Args: pic (PIL.Image or numpy.ndarray): the image to be converted to tensor.
            Returns: Tensor: Converted image.
        """

        image = self.to_tensor(image)/255

        if isinstance(depth, np.ndarray):
            depth = self.to_tensor(depth)/50
        else:
            depth = self.to_tensor(depth)/100000
            
        try:
            if isinstance(vhm, np.ndarray):
                vhm = self.to_tensor(vhm)/50
            else:
                vhm = self.to_tensor(vhm)/100000

        # If no height map has been specified, we construct a uniformly
        # negative heightmap, so that the training will happen on the whole image.

        except AttributeError:
            vhm = -torch.ones_like(depth)


        #vhm = -torch.ones_like(depth)

        return {'image': image, 'depth': depth, 'vhm': vhm}

    def to_tensor(self, pic):

        if isinstance(pic, np.ndarray):

            # Handle numpy tensor, removing the opacity (alpha) channel if present.
            # Note that the alpha channel would have only entries with the '255' value.

            img = torch.from_numpy(pic)
            nchannel = pic.shape[2]

            if nchannel == 4:

                fourth_channel_is_alpha = img[:, :, 3].flatten().sum() == 255 * img[:, :, 3].flatten().size(dim=0)

                if fourth_channel_is_alpha == True:
                    print('Removing alpha channel!')
                    img = torch.from_numpy(pic[:, :, (0, 1, 2)])
                    nchannel = 3

        else:

            # Handle PIL Image

            if pic.mode == 'I':
                img = torch.from_numpy(np.array(pic, np.int32, copy=False))
            elif pic.mode == 'I;16':
                img = torch.from_numpy(np.array(pic, np.int16, copy=False))
            else:
                img = torch.ByteTensor(torch.ByteStorage.from_buffer(pic.tobytes()))

            # PIL image mode: 1, L, P, I, F, RGB, YCbCr, RGBA, CMYK

            if pic.mode == 'YCbCr':
                nchannel = 3
            elif pic.mode == 'I;16':
                nchannel = 1
            else:
                nchannel = len(pic.mode)

            img = img.view(pic.size[1], pic.size[0], nchannel)

        # Put it from HWC to CHW format
        # Yikes, this transpose takes 80% of the loading time/CPU
        img = img.transpose(0, 1).transpose(0, 2).contiguous()

        return img.float()


class Normalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, sample):
        """
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
        Returns:
            Tensor: Normalized image.
        """
        image, depth, vhm = sample['image'], sample['depth'], sample['vhm']

        image = self.normalize(image, self.mean, self.std)

        return {'image': image, 'depth': depth, 'vhm': vhm}

    def normalize(self, tensor, mean, std):
        """Normalize a tensor image with mean and standard deviation.
        See ``Normalize`` for more details.
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
            mean (sequence): Sequence of means for R, G, B channels respecitvely.
            std (sequence): Sequence of standard deviations for R, G, B channels
                respecitvely.
        Returns:
            Tensor: Normalized image.
        """

        # TODO: make efficient
        for t, m, s in zip(tensor, mean, std):
            t.sub_(m).div_(s)

        return tensor
