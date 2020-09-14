import os
import uuid
import re
from shutil import copy
import itertools


files = os.listdir("raw_videos")

only_id = []
for file in files:
    only_id.append(file.split("_")[-1])


pairs = []
for i in range(len(files)):

    key = only_id[i]
    pair = []
    for j in range(len(files)):
        if key in files[j]:
            pair.append(files[j])

    if len(pair) == 2:
        pairs.append(pair)
    else:
        print("not paired because: ",len(pair))
pairs.sort()
pairs = list(pairs for pairs,_ in itertools.groupby(pairs))
print(pairs)

print(len(pairs))
for pair in pairs:
    dir = "video_done/"+str(uuid.uuid4())
    os.makedirs(dir)

    first = re.sub("[^0-9]", "",pair[0].split('_')[0])
    second = re.sub("[^0-9]", "",pair[1].split('_')[0])

    if int(first) > int(second):
        copy(os.path.join('raw_videos',pair[0]) , os.path.join(dir,"high.mp4"))
        copy(os.path.join('raw_videos',pair[1]) , os.path.join(dir,"low.mp4"))
    else:
        copy(os.path.join('raw_videos',pair[1]) , os.path.join(dir,"high.mp4"))
        copy(os.path.join('raw_videos',pair[0]) , os.path.join(dir,"low.mp4"))

    os.remove(os.path.join('raw_videos',pair[0]))
    os.remove(os.path.join('raw_videos',pair[1]))