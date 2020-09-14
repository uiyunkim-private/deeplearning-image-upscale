from ISR.models import RRDN
from ISR.models import Discriminator
from ISR.models import Cut_VGG19
import os


# os.remove('logs')
# os.remove('weights')
# os.makedirs('logs')
# os.makedirs('weights')

lr_train_patch_size = 40
layers_to_extract = [5, 9]
scale = 2
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
loss_weights = {
  'generator': 0.1,
  'feature_extractor': 0.9,
  'discriminator': 0
}



losses = {
  'generator': 'mae',
  'feature_extractor': 'mse',
  'discriminator': 'binary_crossentropy'
}

log_dirs = {'logs': './logs', 'weights': './weights'}

learning_rate = {'initial_value': 0.0004, 'decay_factor': 0.5, 'decay_frequency': 30}

flatness = {'min': 0.0, 'max': 0.15, 'increase': 0.01, 'increase_frequency': 5}


weights_generator_path = "weights/rrdn-C4-D3-G64-G064-T10-x2/2020-09-11_0031/rrdn-C4-D3-G64-G064-T10-x2_best-val_generator_PSNR_Y_epoch014.hdf5"
weights_discriminator_path = "weights/rrdn-C4-D3-G64-G064-T10-x2/2020-09-11_0031/srgan-large_best-val_generator_PSNR_Y_epoch014.hdf5"
trainer = Trainer(
    generator=rrdn,
    discriminator=discr,
    feature_extractor=f_ext,
    lr_train_dir='dataset/low_res/training',
    hr_train_dir='dataset/high_res/training',
    lr_valid_dir='dataset/low_res/validation',
    hr_valid_dir='dataset/high_res/validation',
    loss_weights=loss_weights,
    learning_rate=learning_rate,
    flatness=flatness,
    dataname='image_dataset',
    log_dirs=log_dirs,
    weights_generator=weights_generator_path,
    weights_discriminator=weights_discriminator_path,
    n_validation=40,
)

trainer.train(
    epochs=210,
    steps_per_epoch=1000,
    batch_size=16,
    monitored_metrics={'val_feature_extractor_loss': 'min'}
)