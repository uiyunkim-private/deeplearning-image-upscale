import os
import tqdm


dataset_dir = r"G:\내 드라이브\storage\dataset\dlss\"

lr_train_dir = dataset_dir + '/low_res/training'
hr_train_dir = dataset_dir + '/high_res/training'

# for data in list:


hr = os.listdir(hr_train_dir)
lr = os.listdir(lr_train_dir)

mismatch = [x for x in tqdm.tqdm(hr) if x not in lr]
mismatch2 = [x for x in tqdm.tqdm(lr) if x not in hr]

for data in mismatch:
    if os.path.exists(hr_train_dir +'/'+ data):
        os.remove(hr_train_dir +'/'+ data)

for data in mismatch2:
    if os.path.exists(lr_train_dir + '/' + data):
        os.remove(lr_train_dir + '/' + data)


exit(1)
lr_valid_dir = dataset_dir + '/low_res/validation'
hr_valid_dir = dataset_dir + '/high_res/validation'
