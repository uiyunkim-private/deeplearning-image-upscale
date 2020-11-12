import numpy as np
from PIL import Image
img = Image.open('image3.jpg')
lr_img = np.array(img)

from ISR.models import RRDN

rrdn = RRDN(arch_params={'C':4, 'D':3, 'G':64, 'G0':64, 'T':10, 'x':4})

rrdn.model.load_weights(r"C:\Users\home\Documents\GitHub\deeplearning-image-upscale\weights\rrdn-C4-D3-G64-G064-T10-x4\2020-10-26_1140\rrdn-C4-D3-G64-G064-T10-x4_epoch253.hdf5")

lr_img = rrdn.predict(lr_img,padding_size=200)
Image.fromarray(lr_img).save('result.png')
