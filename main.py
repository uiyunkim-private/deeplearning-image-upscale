import numpy as np
from PIL import Image
import tensorflow as tf
img = Image.open('image.jpg')
lr_img = np.array(img)

from ISR.models import RRDN

#rrdn = RRDN(weights='gans')

rrdn = RRDN(arch_params={'C':4, 'D':3, 'G':32, 'G0':32, 'T':10, 'x':4})

rrdn.model.load_weights(r"C:\Users\home\Documents\GitHub\deeplearning-image-upscale\weights\rrdn-C4-D3-G32-G032-T10-x4\2020-10-21_0340\rrdn-C4-D3-G32-G032-T10-x4_epoch055.hdf5")

lr_img = rrdn.predict(lr_img)
Image.fromarray(lr_img).save('result2.png')
