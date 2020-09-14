
import cv2
import os
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
import cv2
import multiprocessing
import os
import sys


def extract_video(path):
    code = os.path.basename(path).split('_')[1]
    files = os.listdir(path)

    if len(files) != 2:
        print("error")

    low_res_file = "low.mp4"
    high_res_file = "high.mp4"
    video_num = code
    print("Processing Video: ",video_num)

    by_video_path = os.path.join(os.getcwd(),'dataset','by_video',video_num)
    if os.path.exists(by_video_path):
        print("already extracted. PASS\n")
        return
    if not os.path.exists(os.path.join(by_video_path,'low_res','training')):
        os.makedirs(os.path.join(by_video_path,'low_res','training'))
    if not os.path.exists(os.path.join(by_video_path, 'low_res', 'validation')):
        os.makedirs(os.path.join(by_video_path, 'low_res', 'validation'))
    if not os.path.exists(os.path.join(by_video_path,'high_res','training')):
        os.makedirs(os.path.join(by_video_path,'high_res','training'))
    if not os.path.exists(os.path.join(by_video_path, 'high_res', 'validation')):
        os.makedirs(os.path.join(by_video_path, 'high_res', 'validation'))

    print(path,"HIGH RES: ",high_res_file)
    print(path,"low res: ",low_res_file)

    high_res_video_path = os.path.join(path,high_res_file)
    print(high_res_video_path)

    cap = cv2.VideoCapture(high_res_video_path)
    i = 0

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i % 150 == 0:
            cv2.imwrite(os.path.join(by_video_path,'high_res','training',code +str(i) + '.jpg') , frame)
        if i % 1350 == 675:
            cv2.imwrite(os.path.join(by_video_path, 'high_res', 'validation', code + str(i) + '.jpg'), frame)
        i += 1

    cap.release()
    cv2.destroyAllWindows()

    low_res_video_path = os.path.join(path,low_res_file)
    print(low_res_video_path)
    cap = cv2.VideoCapture(low_res_video_path)
    i = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i % 150 == 0:
            cv2.imwrite(os.path.join(by_video_path,'low_res','training',code +str(i) + '.jpg') , frame)
        if i % 1350 == 675:
            cv2.imwrite(os.path.join(by_video_path, 'low_res', 'validation', code + str(i) + '.jpg'), frame)
        i += 1

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    for folder in os.listdir("pornhub_videos"):
        extract_video(os.path.join("pornhub_videos",folder))


