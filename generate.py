
import cv2
import os
from configuration import DIR_DATASETS, DIR_PROCESSED
import json
import shutil
from tqdm import tqdm
from multiprocessing import Pool,Lock
import random
from pathlib import Path
lock = Lock()

class dataset_generator:
    
    def __init__(self,search_root,dataset_dir,dict_filter):

        self.dir_search_root = search_root
        self.dir_dataset = dataset_dir
        self.dict_filter = dict_filter

        self.list_defected = []

    def method_generator(self):
        self.method_initialize_database()
        self.method_filter()
        self.method_pair()
        self.method_extract()
        print(len(self.list_defected)," Defected.")
        print(self.list_defected)
        

    def method_initialize_database(self):
        print("Initializing Database")
        if not os.path.exists(self.dir_dataset):
            os.makedirs(self.dir_dataset)

        if os.path.exists(os.path.join(self.dir_dataset,'database.txt')):
            with open(os.path.join(self.dir_dataset,'database.txt')) as file_database:
                self.list_database = json.load(file_database)
        else:
            with open(os.path.join(self.dir_dataset,'database.txt'), 'w') as file_database:
                self.list_database = []
                json.dump([], file_database)

    def thread_filter(self,_id):

        path_file_meta_data = os.path.join(self.dir_search_root,_id,'meta.txt')

        try:
            with open(path_file_meta_data) as file_meta_data:
                dict_meta_data = json.load(file_meta_data)
        except Exception as e:
            self.list_defected.append(_id)
            print("[Exception] Failed To Load Metadata. Skipping ",_id)
            return _id, False

        list_id_filtered = []

        if not self.dict_filter['max_duration'] > dict_meta_data['duration'] > self.dict_filter['min_duration']:
            return _id, False
        
        list_keywords_to_search = []
        for x in [x.lower() for x in dict_meta_data['tags'] + dict_meta_data['categories'] + dict_meta_data['title'].split(' ')]:
            list_keywords_to_search =list_keywords_to_search + x.split(' ')
        return _id, len([x for x in list_keywords_to_search if x in self.dict_filter['keywords']]) != 0

    def method_filter(self):
        print("Filtering")
        list_id = [x for x in os.listdir(self.dir_search_root) if not x.startswith('temp_')]
        print(len(list_id)," Found. Comparing With Database")
        list_id_not_exist = [x for x in list_id if x not in self.list_database]
        print(len(list_id_not_exist)," Processing. Duplicates Removed")
        with Pool() as p:
            list_tuple_id_filtered =list(
                                         tqdm(
                                              p.imap(
                                                     self.thread_filter,list_id_not_exist
                                                    ),
                                              total=len(list_id_not_exist),
                                              )
                                        )

        
        self.list_id_filtered = [x[0] for x in list_tuple_id_filtered if x[1]]

    def thread_pair(self,_id):
        
        list_path_files = [os.path.join(self.dir_search_root,_id,x) for x in os.listdir(os.path.join(self.dir_search_root,_id))]

        list_file_high_res = [x for x in list_path_files if x.split('.')[-2].endswith(str(self.dict_filter['high_res']))]
        list_file_low_res = [x for x in list_path_files if x.split('.')[-2].endswith(str(self.dict_filter['low_res']))]

        if len(list_file_high_res) == 1:
            file_high_res = list_file_high_res[0]
        else:
            self.list_defected.append(_id)
            file_high_res = None

        if len(list_file_low_res) == 1:
            file_low_res = list_file_low_res[0]
        else:
            self.list_defected.append(_id)
            print(list_file_low_res)
            file_low_res = None

        return {'id':_id,'high_res':file_high_res,'low_res':file_low_res}



    def method_pair(self):
        print("Pairing")
        with Pool() as p:
            self.list_dict_paired_path =list(
                                             tqdm(
                                                  p.imap(self.thread_pair,self.list_id_filtered),
                                                  total=len(self.list_id_filtered)
                                                  )
                                            )

    def thread_extract(self,_dict_pair):
        
        try:
            for resolution in ['high_res','low_res']:
                
                print("Start Extracting")
                lock.acquire()
                dir_save = os.path.join(self.dir_dataset,_dict_pair['id'],resolution)
                if not os.path.exists(dir_save):
                    os.makedirs(dir_save)
                lock.release()
                frames = []
                cap = cv2.VideoCapture(_dict_pair[resolution])
                count = 0
                while (cap.isOpened()):
                    ret, frame = cap.read()
                    if not ret:
                        break

                    if count % 150 == 13:
                        if resolution == 'low_res':
                            new_shape=( int(x_high_res/self.dict_filter['scale_factor']),int(y_high_res/self.dict_filter['scale_factor'])  )
                            frame = cv2.resize(frame,dsize=new_shape,interpolation=cv2.INTER_CUBIC)
                        frames.append(frame)

                    count += 1
                
                for i,frame in enumerate(frames):
                    cv2.imwrite(os.path.join(dir_save,_dict_pair['id'] +str(i) + '.png') , frame)

                if resolution == 'high_res':
                    file_high_res_sample = os.listdir(dir_save)[0]
                    image_high_res_sample = cv2.imread(os.path.join(dir_save,file_high_res_sample))
                    y_high_res = image_high_res_sample.shape[0]
                    x_high_res = image_high_res_sample.shape[1]

                cap.release()

        except Exception as e:
            self.list_defected.append(_dict_pair['id'])
            print("[Exception] Failed To Extract Frame. Deleting",_dict_pair['id'])
            print(e)
            if os.path.exists(os.path.join(self.dir_dataset,_dict_pair['id'])):
                shutil.rmtree(os.path.join(self.dir_dataset,_dict_pair['id']))
        else:
            list_dir_high_res = os.listdir(os.path.join(self.dir_dataset,_dict_pair['id'],'high_res'))
            list_dir_low_res = os.listdir(os.path.join(self.dir_dataset,_dict_pair['id'],'low_res'))

            if len(list_dir_high_res) == len(list_dir_low_res):
                list_random_indexes = random.sample(range(len(list_dir_high_res)), int(len(list_dir_high_res) * 0.1))
                
                dict_dataset = {}

                dict_dataset.update(
                                        {
                                            'high_res':{
                                                            'train':[list_dir_high_res[i] for i in range(len(list_dir_high_res)) if not i in list_random_indexes],
                                                            'validation': [list_dir_high_res[i] for i in range(len(list_dir_high_res)) if  i in list_random_indexes]
                                                       },

                                            'low_res':{
                                                            'train':[list_dir_low_res[i] for i in range(len(list_dir_low_res)) if not i in list_random_indexes],
                                                            'validation': [list_dir_low_res[i] for i in range(len(list_dir_low_res)) if  i in list_random_indexes]
                                                      }
                                                 
                                        } 
                                   )
                
                try:
                    for resolution in ['high_res','low_res']:
                        for dataset in ['train','validation']:
                            dir_extracted = os.path.join(self.dir_dataset,_dict_pair['id'],resolution)
                            dir_dataset = os.path.join(self.dir_dataset,resolution,dataset)

                            lock.acquire()
                            if not os.path.exists(dir_dataset):
                                os.makedirs(dir_dataset)
                            lock.release()
                            
                            for file in dict_dataset[resolution][dataset]:
                                shutil.copy(os.path.join(dir_extracted,file),os.path.join(dir_dataset,file))
                except Exception as e:
                    self.list_defected.append(_dict_pair['id'])
                    print("[Exception] Failed To Copying File to Dataset Folder ",_dict_pair['id'])

                shutil.rmtree(os.path.join(self.dir_dataset,_dict_pair['id']))
                lock.acquire()

                with open(os.path.join(self.dir_dataset,'database.txt')) as file_database:
                    self.list_database = json.load(file_database)
                
                self.list_database.append(_dict_pair['id'])

                with open(os.path.join(self.dir_dataset,'database.txt'), 'w') as file_database:
                    json.dump(self.list_database, file_database)

                lock.release()
            else:
                self.list_defected.append(_dict_pair['id'])
                print("[Exception] Integrity Problem",_dict_pair['id'])
                if os.path.exists(os.path.join(self.dir_dataset,_dict_pair['id'])):
                    shutil.rmtree(os.path.join(self.dir_dataset,_dict_pair['id']))

        return True


    def method_extract(self):
        print("Extracting")
        random.shuffle(self.list_dict_paired_path)
        for _dict_paired_path in tqdm(self.list_dict_paired_path):
            self.thread_extract(_dict_paired_path)

        # with Pool(4) as p:
        #     list(tqdm(p.imap(self.thread_extract,self.list_dict_paired_path),total=len(self.list_dict_paired_path)))

if __name__ == '__main__':



    generator = dataset_generator(
                                  search_root=DIR_DATASETS,
                                  dataset_dir=DIR_PROCESSED,
                                  dict_filter={
                                               'max_duration':1500,
                                               'min_duration':700, 
                                               'high_res':1080,
                                               'low_res':240,
                                               'scale_factor':4
                                              }
                                 )
    generator.method_generator()


