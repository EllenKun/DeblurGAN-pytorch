import os
import random

import torch
from PIL import Image
from torch.utils.data import Dataset


class GoProDataset(Dataset):
    """
    GoPro dataset
    """

    def __init__(self, data_dir='data', transform=None, height=360, width=640, fine_size=256):
        self.blurred_dir = os.path.join(data_dir, 'blurred')
        self.sharp_dir = os.path.join(data_dir, 'sharp')
        self.image_names = os.listdir(self.blurred_dir)  # we assume that blurred and sharp images have the same names

        self.transform = transform

        assert height >= fine_size and width >= fine_size
        self.height = height
        self.width = width
        self.fine_size = fine_size

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, index):
        blurred = Image.open(os.path.join(self.blurred_dir, self.image_names[index])).convert('RGB')
        sharp = Image.open(os.path.join(self.sharp_dir, self.image_names[index])).convert('RGB')

        if self.transform:
            blurred = self.transform(blurred)
            sharp = self.transform(sharp)

            # crop image tensor to defined size
            # we assume that self.transform contains ToTensor()
            assert isinstance(blurred, torch.Tensor) and isinstance(sharp, torch.Tensor)
            h_offset = random.randint(0, self.height - self.fine_size)
            w_offset = random.randint(0, self.width - self.fine_size)
            blurred = blurred[:, h_offset:h_offset + self.fine_size, w_offset:w_offset + self.fine_size]
            sharp = sharp[:, h_offset:h_offset + self.fine_size, w_offset:w_offset + self.fine_size]
        return {'blurred': blurred, 'sharp': sharp}


class CustomDataset(Dataset):
    """Custom dataset for image deblurring"""

    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform

        self.image_names = os.listdir(self.data_dir)

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, index):
        image_name = self.image_names[index]
        blurred = Image.open(os.path.join(self.data_dir, image_name)).convert('RGB')

        if self.transform:
            blurred = self.transform(blurred)

        return {'blurred': blurred, 'image_name': image_name}
