import requests
import time
import youtube_dl
import threading
import uuid
import os
import shutil
from selenium import webdriver


def download():
    task_id = str(uuid.uuid4())
    try:
        head_url = 'http://pornhub.com/video/random'
        r = requests.get(head_url)
        url = r.url
    except:
        print("url error")
        return
    print(url)

    ydl = youtube_dl.YoutubeDL({})

    try:
        meta = ydl.extract_info(url, download=False)
    except:
        print("Pornhub error")
        return

    duration = int(meta['duration'])
    all_formats = meta['formats']

    if duration > 600 and duration < 1200:
        exist_240 = list(filter(lambda format: format['format_id'] == '240p', all_formats))
        exist_480 = list(filter(lambda format: format['format_id'] == '480p', all_formats))
        exist_720 = list(filter(lambda format: format['format_id'] == '720p', all_formats))
        exist_1080 = list(filter(lambda format: format['format_id'] == '1080p', all_formats))
        code = (len(exist_240) == 1, len(exist_480) == 1, len(exist_720) == 1, len(exist_1080) == 1)
        print("existance: ", code)
        task_folder = os.path.join("pornhub_videos", task_id)
        if code[1] and code[3]:
            try:
                if not os.path.exists(task_folder):
                    os.makedirs(task_folder)

                tmp_url = exist_480[0]['url']
                r = requests.get(tmp_url, allow_redirects=True)
                open(os.path.join(task_folder, "low.mp4"), 'wb').write(r.content)

                tmp_url = exist_1080[0]['url']
                r = requests.get(tmp_url, allow_redirects=True)
                open(os.path.join(task_folder, "high.mp4"), 'wb').write(r.content)
                os.rename(task_folder, os.path.join(os.path.dirname(task_folder), '0_' + task_id))
            except:
                print("error happen when downloading")
                if os.path.exists(task_folder):
                    shutil.rmtree(task_folder)

                                 

def worker():

    while(True):
        download()




threads = []
for i in range(20):
    t = threading.Thread(target=worker)
    threads.append(t)

    t.start()
    time.sleep(60)



