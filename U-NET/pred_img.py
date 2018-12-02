import os

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pickle
from skimage.io import imread
from scipy.misc import imresize
from keras import backend as K
from keras.callbacks import ModelCheckpoint, CSVLogger
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.optimizers import Adam
from skimage.io import imsave
from PIL import Image, ImageOps

#from data import load_train_data, load_test_data

K.set_image_data_format('channels_last')  # TF dimension ordering in this code

imagens = [x for x in os.listdir(os.path.join('imgs/real'))]
output_path = os.path.join('imgs/real')

proporcao = 0.65
#proporcao = 0.50
image = np.array(Image.open(os.path.join('imgs/real', imagens[0])).convert('L'))
proporcao_resize = ((int(np.floor(proporcao*image.shape[0])//16)*16),(int(np.floor(proporcao*image.shape[1])//16)*16))

img_rows = proporcao_resize[0]
img_cols = proporcao_resize[1]

smooth = 1.
batchsize = 11

def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)

def get_unet():
    inputs = Input((img_rows, img_cols, 1))
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

    up6 = concatenate([UpSampling2D(size=(2, 2))(conv5), conv4], axis=3)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(up6)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

    up7 = concatenate([UpSampling2D(size=(2, 2))(conv6), conv3], axis=3)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(up7)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

    up8 = concatenate([UpSampling2D(size=(2, 2))(conv7), conv2], axis=3)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(up8)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv8)

    up9 = concatenate([UpSampling2D(size=(2, 2))(conv8), conv1], axis=3)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(up9)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv9)

    conv10 = Conv2D(1, (1, 1), activation='sigmoid')(conv9)

    model = Model(inputs=[inputs], outputs=[conv10])
    model.compile(optimizer=Adam(lr=1e-5), loss=dice_coef_loss,
                  metrics=['accuracy'])
    model.summary()

    return model

bit = 8

model = get_unet()

print('-' * 30)
print('Loading saved weights...')
print('-' * 30)
model.load_weights('weights_unet_' + str(bit) + '.h5')
    
imagens_redim = [imresize(np.array(Image.open(os.path.join('imgs/real', x)).convert('L')),proporcao_resize,interp='bicubic',mode='L') for x in imagens]
imagens_redim = np.array([np.expand_dims(x,axis=2) for x in imagens_redim])

#with open('norm_params.pkl', 'wb') as fl:
#    mean, std = pickle.load(fl)

imagens_redim = imagens_redim.astype('float32')
mean = np.mean(imagens_redim)
std = np.std(imagens_redim)

imagens_redim -= mean
imagens_redim /= std

print("Cleaning selected images...")
results = []
i = 0
tot = len(imagens_redim)
for img in imagens_redim:
    results.append(model.predict(np.array(np.expand_dims(img,axis=0)),verbose=0)[0])
    print('\r%3.2f%% concluído'%((i+1)*100/tot),end='')
    i+=1
print('')
#results = model.predict(imagens_redim, verbose=1)

results = [(x * 255.).astype(np.uint8) for x in results]
print("Converting results")
pil_results = [ImageOps.invert(Image.fromarray(imresize(x[:,:,0],(image.shape[0],image.shape[1]),interp='bicubic',mode='L'))) for x in results]
print("Saving results")
for img in range(len(pil_results)):
    pil_results[img].save(output_path+'/'+imagens[img].strip('.jpg')+'_treated.jpg',"JPEG")
    print('\r%3.2f%% concluído'%((img+1)*100/tot),end='')
