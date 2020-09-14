import os
from shutil import copyfile, rmtree
import cv2

def inspect_dataset(path):
    high_train = os.path.join(path, 'high_res', 'training')
    high_val = os.path.join(path, 'high_res', 'validation')

    low_train = os.path.join(path, 'low_res', 'training')
    low_val = os.path.join(path, 'low_res', 'validation')

    if len(os.listdir(high_train)) != len(os.listdir(low_train)):
        print(path," has integrity problem")
        return False

    if len(os.listdir(high_val)) != len(os.listdir(low_val)):
        print(path," has integrity problem")
        return False

    first_high_frame = cv2.imread(os.path.join(high_train,os.listdir(high_train)[0]))
    first_low_frame = cv2.imread(os.path.join(low_train,os.listdir(low_train)[0]))

    if not first_high_frame.shape[0] > first_low_frame.shape[0]:
        print("switched low-high detected",path)
        return False

    print("Integrity test passed")
    return True

def move_dataset(path):


    high_train_dataset_path = os.path.join('dataset','high_res','training')
    high_val_dataset_path = os.path.join('dataset', 'high_res', 'validation')
    low_train_dataset_path = os.path.join('dataset','low_res','training')
    low_val_dataset_path = os.path.join('dataset', 'low_res', 'validation')

    high_train = os.path.join(path, 'high_res', 'training')
    high_val = os.path.join(path, 'high_res', 'validation')
    low_train = os.path.join(path, 'low_res', 'training')
    low_val = os.path.join(path, 'low_res', 'validation')


    high_shape = cv2.imread(os.path.join(high_train, os.listdir(high_train)[0])).shape

    shapex = high_shape[0]
    shapey = high_shape[1]

    half_shapex = int(shapex / 2)
    half_shapey = int(shapey / 2)
    if half_shapex * 2 != shapex or half_shapey * 2 != shapey:
        print("video can't be resized half")
        return

    for file in os.listdir(high_train):
        file_path = os.path.join(high_train,file)
        if not os.path.exists(os.path.join(high_train_dataset_path,file)):
            img = cv2.imread(file_path)
            img = cv2.resize(img,dsize=(shapey,shapex))
            cv2.imwrite(os.path.join(high_train_dataset_path,file),img)
            #copyfile(file_path,os.path.join(high_train_dataset_path,file),img )
        else:
            print("file exists: " ,file_path)
    for file in os.listdir(high_val):
        file_path = os.path.join(high_val,file)
        if not os.path.exists(os.path.join(high_val_dataset_path,file)):
            img = cv2.imread(file_path)
            img = cv2.resize(img,dsize=(shapey,shapex))
            cv2.imwrite(os.path.join(high_val_dataset_path,file),img)
            #copyfile(file_path, os.path.join(high_val_dataset_path,file))
        else:
            print("file exists: " ,file_path)
    for file in os.listdir(low_train):
        file_path = os.path.join(low_train,file)
        if not os.path.exists(os.path.join(low_train_dataset_path,file)):
            img = cv2.imread(file_path)
            img = cv2.resize(img,dsize=(half_shapey,half_shapex))
            cv2.imwrite(os.path.join(low_train_dataset_path,file),img)
            #copyfile(file_path, os.path.join(low_train_dataset_path,file))
        else:
            print("file exists: " ,file_path)
    for file in os.listdir(low_val):
        file_path = os.path.join(low_val,file)
        if not os.path.exists(os.path.join(low_val_dataset_path,file)):
            img = cv2.imread(file_path)
            img = cv2.resize(img,dsize=(half_shapey,half_shapex))
            cv2.imwrite(os.path.join(low_val_dataset_path,file),img)
            #copyfile(file_path, os.path.join(low_val_dataset_path,file))
        else:
            print("file exists: " ,file_path)


if not os.path.exists("dataset/high_res/training"):
    os.makedirs("dataset/high_res/training")
if not os.path.exists("dataset/high_res/validation"):
    os.makedirs("dataset/high_res/validation")
if not os.path.exists("dataset/low_res/training"):
    os.makedirs("dataset/low_res/training")
if not os.path.exists("dataset/low_res/validation"):
    os.makedirs("dataset/low_res/validation")


hi_res_train_path = "dataset/high_res/training"
hi_res_val_path = "dataset/high_res/validation"
low_res_train_path = "dataset/low_res/training"
low_res_val_path = "dataset/low_res/validation"

seperated_dataset_dir = os.path.join('dataset','by_video')

for each in os.listdir(seperated_dataset_dir):
    each_path = os.path.join(seperated_dataset_dir,each)

    if inspect_dataset(each_path):
        move_dataset(each_path)
