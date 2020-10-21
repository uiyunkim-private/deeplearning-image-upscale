import os
import tqdm
list = ['ph574153cb2770c106', 'ph574153cb2770c107', 'ph574153cb2770c11', 'ph574153cb2770c111', 'ph574153cb2770c112', 'ph574153cb2770c113', 'ph574153cb2770c114', 'ph574153cb2770c115', 'ph574153cb2770c116', 'ph574153cb2770c117', 'ph574153cb2770c12', 'ph574153cb2770c13', 'ph574153cb2770c14', 'ph574153cb2770c15', 'ph574153cb2770c16', 'ph574153cb2770c17', 'ph574153cb2770c18', 'ph574153cb2770c19', 'ph574153cb2770c2', 'ph574153cb2770c20', 'ph574153cb2770c21', 'ph574153cb2770c23', 'ph574153cb2770c24', 'ph574153cb2770c25', 'ph574153cb2770c26', 'ph574153cb2770c27', 'ph574153cb2770c29', 'ph574153cb2770c3', 'ph574153cb2770c30', 'ph574153cb2770c31', 'ph574153cb2770c32', 'ph574153cb2770c33', 'ph574153cb2770c34', 'ph574153cb2770c35', 'ph574153cb2770c36', 'ph574153cb2770c37', 'ph574153cb2770c38', 'ph574153cb2770c39', 'ph574153cb2770c4', 'ph574153cb2770c40', 'ph574153cb2770c41', 'ph574153cb2770c42', 'ph574153cb2770c43', 'ph574153cb2770c44', 'ph574153cb2770c46', 'ph574153cb2770c47', 'ph574153cb2770c48', 'ph574153cb2770c49', 'ph574153cb2770c5', 'ph574153cb2770c50', 'ph574153cb2770c51', 'ph574153cb2770c52', 'ph574153cb2770c53', 'ph574153cb2770c54', 'ph574153cb2770c55', 'ph574153cb2770c56', 'ph574153cb2770c57', 'ph574153cb2770c58', 'ph574153cb2770c59', 'ph574153cb2770c6', 'ph574153cb2770c60', 'ph574153cb2770c61', 'ph574153cb2770c62', 'ph574153cb2770c65', 'ph574153cb2770c66', 'ph574153cb2770c67', 'ph574153cb2770c68', 'ph574153cb2770c69', 'ph574153cb2770c7', 'ph574153cb2770c70', 'ph574153cb2770c71', 'ph574153cb2770c72', 'ph574153cb2770c73', 'ph574153cb2770c74', 'ph574153cb2770c75', 'ph574153cb2770c76', 'ph574153cb2770c78', 'ph574153cb2770c79', 'ph574153cb2770c83', 'ph574153cb2770c84', 'ph574153cb2770c85', 'ph574153cb2770c86', 'ph574153cb2770c87', 'ph574153cb2770c88', 'ph574153cb2770c89', 'ph574153cb2770c9', 'ph574153cb2770c90', 'ph574153cb2770c91', 'ph574153cb2770c92', 'ph574153cb2770c93', 'ph574153cb2770c94', 'ph574153cb2770c95', 'ph574153cb2770c96', 'ph574153cb2770c97', 'ph574153cb2770c98', 'ph585ade4e4c751102', 'ph585ade4e4c751103', 'ph585ade4e4c751104', 'ph585ade4e4c751111', 'ph585ade4e4c751113', 'ph585ade4e4c751114', 'ph585ade4e4c751115', 'ph585ade4e4c751116', 'ph585ade4e4c751118', 'ph585ade4e4c751119', 'ph585ade4e4c75112', 'ph585ade4e4c751120', 'ph585ade4e4c751121', 'ph585ade4e4c751122', 'ph585ade4e4c751123', 'ph585ade4e4c751124', 'ph585ade4e4c751125', 'ph585ade4e4c751126', 'ph585ade4e4c751127', 'ph585ade4e4c751128', 'ph585ade4e4c751129', 'ph585ade4e4c75113', 'ph585ade4e4c751130', 'ph585ade4e4c751131', 'ph585ade4e4c751133', 'ph585ade4e4c751134', 'ph585ade4e4c751135', 'ph585ade4e4c751136', 'ph585ade4e4c751137', 'ph585ade4e4c751138', 'ph585ade4e4c751139', 'ph585ade4e4c75114', 'ph585ade4e4c751141', 'ph585ade4e4c751142', 'ph585ade4e4c751143', 'ph585ade4e4c75115', 'ph585ade4e4c75116', 'ph585ade4e4c75117', 'ph585ade4e4c75118', 'ph585ade4e4c75119', 'ph585ade4e4c7512', 'ph585ade4e4c75120', 'ph585ade4e4c75121', 'ph585ade4e4c75122', 'ph585ade4e4c75123', 'ph585ade4e4c75124', 'ph585ade4e4c75125', 'ph585ade4e4c75126', 'ph585ade4e4c75127', 'ph585ade4e4c75128', 'ph585ade4e4c75129', 'ph585ade4e4c7513', 'ph585ade4e4c75130', 'ph585ade4e4c75131', 'ph585ade4e4c75133', 'ph585ade4e4c75134', 'ph585ade4e4c75135', 'ph585ade4e4c75136', 'ph585ade4e4c75138', 'ph585ade4e4c75139', 'ph585ade4e4c7514', 'ph585ade4e4c75140', 'ph585ade4e4c75141', 'ph585ade4e4c75142', 'ph585ade4e4c75143', 'ph585ade4e4c75144', 'ph585ade4e4c75145', 'ph585ade4e4c75147', 'ph585ade4e4c75148', 'ph585ade4e4c75149', 'ph585ade4e4c7515', 'ph585ade4e4c75150', 'ph585ade4e4c75151', 'ph585ade4e4c75152', 'ph585ade4e4c75153', 'ph585ade4e4c75154', 'ph585ade4e4c75155', 'ph585ade4e4c75156', 'ph585ade4e4c75157', 'ph585ade4e4c75158', 'ph585ade4e4c75159', 'ph585ade4e4c7516', 'ph585ade4e4c75160', 'ph585ade4e4c75161', 'ph585ade4e4c75162', 'ph585ade4e4c75163', 'ph585ade4e4c75164', 'ph585ade4e4c75165', 'ph585ade4e4c75166', 'ph585ade4e4c75167', 'ph585ade4e4c75168', 'ph585ade4e4c75169', 'ph585ade4e4c7517', 'ph585ade4e4c75171', 'ph585ade4e4c75172', 'ph585ade4e4c75173', 'ph585ade4e4c75174', 'ph585ade4e4c75175', 'ph585ade4e4c75176', 'ph585ade4e4c75177', 'ph585ade4e4c75178', 'ph585ade4e4c75179', 'ph585ade4e4c7518', 'ph585ade4e4c75181', 'ph585ade4e4c75191', 'ph585ade4e4c75192', 'ph585ade4e4c75193', 'ph585ade4e4c75195']


dataset_dir = r"G:\내 드라이브\storage\dataset\dlss\pornhub_x4"

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