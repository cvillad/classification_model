#!/usr/bin/env python

import argparse
import os
import matplotlib.pyplot as plt 
import cv2
import numpy as np
import torch
from tqdm import tqdm
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y

def create_dataset(data_path, names_path, new_path):
    txt_files = [os.path.join(data_path,file) for file in os.listdir(data_path) if 'txt' in file]
    img_files = [os.path.join(data_path,file) for file in os.listdir(data_path) if 'jpg' in file]

    with open(names_path) as file:
        classes = file.readlines()
    classes = [c.rstrip('\n') for c in classes]
    #Class, x, x, y, y
    #for label in txt_files:
    #for label in txt_files
    label = txt_files[22]
    img_names = np.zeros((20,)).astype(int)
    for label_number,label in tqdm(enumerate(txt_files)):
        temp=label.split('.')[0]
        file_name = temp.split('/')[-1]+'.jpg'
        with open(label) as file:
            img = cv2.imread(os.path.join(data_path, file_name)) #opening img file
            h, w = img.shape[:2]
            lines = file.readlines()
            for line in lines:
                x = np.array(line.split()[1:]).astype(float)
                i = int(line.split()[0])
                b = x * [w, h, w, h]  # box
                #b[2:] = b[2:].max()  # rectangle to square
                #b[2:] = b[2:] * 1.3 + 30  # pad
                b = xywh2xyxy(b.reshape(-1, 4)).ravel().astype(np.int)
                b[[0, 2]] = np.clip(b[[0, 2]], 0, w)  # clip boxes outside of image
                b[[1, 3]] = np.clip(b[[1, 3]], 0, h)
                
                new_image = os.path.join(new_path,classes[i])
                if not os.path.exists(new_image):
                    os.makedirs(new_image)
                new_image = os.path.join(new_image,str(img_names[i])+'.jpg')
                cv2.imwrite(new_image, img[b[1]:b[3], b[0]:b[2]]), 'Failure extracting classifier boxes'
                img_names[i]+=1

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data',type=str, default='data/obj_train_data', help='jpg and txt files directory')
    parser.add_argument('--names', type=str, default='data/obj.names', help='file that contains name for each class')
    parser.add_argument('--new-dir', type=str, default='dataset', help='directory where the dataset is going to save')

    args = parser.parse_args()
    data_path = args.data
    names_path = args.names
    new_path = args.new_dir

    create_dataset(data_path, names_path, new_path)
