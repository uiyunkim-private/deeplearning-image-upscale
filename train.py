from ISR.models import RRDN
from ISR.models import Discriminator
from ISR.models import Cut_VGG19
import os

dataset_dir = r"G:\내 드라이브\storage\dataset\dlss\"
# os.remove('logs')
# os.remove('weights')
# os.makedirs('logs')
# os.makedirs('weights')

lr_train_patch_size = 40
layers_to_extract = [5, 9]
scale = 4
hr_train_patch_size = lr_train_patch_size * scale

rrdn  = RRDN(arch_params={'C':4, 'D':3, 'G':64, 'G0':64, 'T':10, 'x':scale}, patch_size=lr_train_patch_size)
f_ext = Cut_VGG19(patch_size=hr_train_patch_size, layers_to_extract=layers_to_extract)
discr = Discriminator(patch_size=hr_train_patch_size, kernel_size=3)

from ISR.train import Trainer

# loss_weights = {
#   'generator': 0.0,
#   'feature_extractor': 0.0833,
#   'discriminator': 0.01
# }
# loss_weights = {
#   'generator': 1.0,
#   'feature_extractor': 0.0833,
#   'discriminator': 0.01
# }
loss_weights = {
  'generator': 1.0,
  'feature_extractor': 0,
  'discriminator': 0
}


losses = {
  'generator': 'mae',
  'feature_extractor': 'mse',
  'discriminator': 'binary_crossentropy'
}

log_dirs = {'logs': './logs', 'weights': './weights'}

learning_rate = {'initial_value': 0.0004, 'decay_factor': 0.5, 'decay_frequency': 50}

flatness = {'min': 0.0, 'max': 0.24, 'increase': 0.01, 'increase_frequency': 3}


weights_generator_path = r"C:\Users\home\Documents\GitHub\deeplearning-image-upscale\weights\rrdn-C4-D3-G64-G064-T10-x4\2020-10-23_0633\rrdn-C4-D3-G64-G064-T10-x4_epoch200.hdf5"
weights_discriminator_path = r"C:\Users\home\Documents\GitHub\deeplearning-image-upscale\weights\rrdn-C4-D3-G64-G064-T10-x4\2020-10-23_0633\srgan-large_epoch200.hdf5"
trainer = Trainer(
    generator=rrdn,
    discriminator=discr,
    feature_extractor=f_ext,
    lr_train_dir=dataset_dir +'/low_res/training',
    hr_train_dir=dataset_dir + '/high_res/training',
    lr_valid_dir=dataset_dir + '/low_res/validation',
    hr_valid_dir=dataset_dir + '/high_res/validation',
    loss_weights=loss_weights,
    learning_rate=learning_rate,
    flatness=flatness,
    dataname='image_dataset',
    log_dirs=log_dirs,
    weights_generator=weights_generator_path,
    weights_discriminator=None,
    n_validation=100,
)

trainer.train(
    epochs=300,
    steps_per_epoch=200,
    batch_size=8,
    monitored_metrics={'val_generator_PSNR_Y': 'min'}
)
