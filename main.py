import numpy as np
from PIL import Image
import tensorflow as tf
img = Image.open('image.jpg')
lr_img = np.array(img)

from ISR.models import RRDN

rrdn = RRDN(weights='gans')

rrdn = RRDN(arch_params={'C':4, 'D':3, 'G':64, 'G0':64, 'T':10, 'x':2})

rrdn.model.load_weights("weights/rrdn-C4-D3-G64-G064-T10-x2/2020-09-11_0031/rrdn-C4-D3-G64-G064-T10-x2_best-val_generator_PSNR_Y_epoch014.hdf5")

lr_img = rrdn.predict(lr_img)
Image.fromarray(lr_img).save('result2.png')
