import os

import numpy as np
from skimage.io import imread
from scipy.misc import imresize

from sklearn.model_selection import train_test_split

raws_pt = [x for x in os.listdir(os.path.join('imgs/teste')) if '_8' in x]
masks_pt = [x for x in os.listdir(os.path.join('imgs/teste')) if 'mask' in x]
train_pt, test_pt = train_test_split([x.replace('_8.jpg','') for x in os.listdir(os.path.join('imgs/teste')) if '_8' in x], test_size=0.1)

proporcao = 0.8
file_name = 'img_00000'
image = imread(os.path.join('imgs/teste', file_name + '_8' + '.jpg'), as_gray=True)
proporcao_resize = ((int(np.floor(proporcao*image.shape[0])//16)*16),(int(np.floor(proporcao*image.shape[1])//16)*16))

train_images = [imresize(imread(os.path.join('imgs\\teste',x+'_8.jpg')),proporcao_resize,interp='bicubic',mode='L') for x in train_pt]
train_masks = [imresize(imread(os.path.join('imgs\\teste',x+'_mask.jpg'))[:,:,0],proporcao_resize,interp='bicubic',mode='L') for x in train_pt]

test_images = [imresize(imread(os.path.join('imgs\\teste',x+'_8.jpg')),proporcao_resize,interp='bicubic',mode='L') for x in test_pt]
test_masks = [imresize(imread(os.path.join('imgs\\teste',x+'_mask.jpg'))[:,:,0],proporcao_resize,interp='bicubic',mode='L') for x in test_pt]

test_train_files = os.path.join('test_train_files')
if not os.path.exists(test_train_files):
    os.mkdir(test_train_files)

np.save(os.path.join(test_train_files,'images_train.npy'), train_images)
np.save(os.path.join(test_train_files,'masks_train.npy'), train_masks)
np.save(os.path.join(test_train_files,'images_test.npy'), test_images)
np.save(os.path.join(test_train_files,'masks_test.npy'), test_masks)

np.save(os.path.join(test_train_files,'images16_train.npy'), train_images)
np.save(os.path.join(test_train_files,'images16_test.npy'), test_images)

np.save(os.path.join(test_train_files,'ids_train.npy'), [x.split('_')[1] for x in train_pt])
np.save(os.path.join(test_train_files,'ids_test.npy'), [x.split('_')[1] for x in test_pt])

print("Feito! Imagens com proporção {}".format(proporcao_resize))