
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, Convolution2D, MaxPooling2D, Dropout, Dense, Flatten, Activation, Input, Reshape, BatchNormalization,Cropping2D
from komponenten.utils import INPUT_SHAPE, batch_generator

import pandas as pd
import numpy as np
import os


test_size = 0.2
keep_prob = 0.5
nb_epoch = 50
samples_per_epoch = 0
batch_size = 40
save_best_only = 'true'
learning_rate = 1.0e-4
data_dir ='data/logs'


np.random.seed(0)

def load_data():
    data_df = pd.read_csv('daten/logs/Log_all.csv', names=['image', 'throttle', 'steering'])

    X = data_df['image'].values
    y = data_df['steering'].values

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=test_size, random_state=0)

    return X_train, X_valid, y_train, y_valid



def build_model_categorical():   

    input_shape=(120, 160, 3)

    drop = 0.2
    
    img_in = Input(shape=input_shape, name='img_in')
    x = img_in
    #x = Cropping2D(cropping=((10,0), (0,0)))(x) #trim 10 pixels off top
    x = Lambda(lambda x: x/127.5 - 1.)(x) # normalize and re-center
    x = Convolution2D(24, (5,5), strides=(2,2), activation='relu', name="conv2d_1")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(32, (5,5), strides=(2,2), activation='relu', name="conv2d_2")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(64, (5,5), strides=(2,2), activation='relu', name="conv2d_3")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(64, (3,3), strides=(1,1), activation='relu', name="conv2d_4")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(64, (3,3), strides=(1,1), activation='relu', name="conv2d_5")(x)
    x = Dropout(drop)(x)
    
    x = Flatten(name='flattened')(x)
    x = Dense(100, activation='relu')(x)
    x = Dropout(drop)(x)
    x = Dense(50, activation='relu')(x)
    x = Dropout(drop)(x)

    out = Dense(15, activation='softmax', name='out')(x)
        
    model = Model(inputs=[img_in], outputs=out)
    
    return model


def build_model_safe():
    

    IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
    INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)

    
    model = Sequential()
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE))
    model.add(Conv2D(24, (5, 5),strides=(2, 2), activation='elu'))
    model.add(Conv2D(36, (5, 5),strides=(2, 2), activation='elu'))
    model.add(Conv2D(48, (3, 3),strides=(2, 2), activation='elu'))
    model.add(Conv2D(64, (3, 3),strides=(2, 2), activation='elu'))
    model.add(Flatten())
    model.add(Dropout(.2))
    model.add(Dense(512, activation='elu'))
    model.add(Dropout(.5))
    model.add(Dense(256, activation='elu'))
    model.add(Dense(128, activation='elu'))
    model.add(Dense(1))
    model.summary()

    return model


def build_model():

    input_shape=(66, 200, 3)

    drop = 0.1
    
    img_in = Input(shape=input_shape, name='img_in')
    x = img_in
    #x = Cropping2D(cropping=((10,0), (0,0)))(x) #trim 10 pixels off top
    x = Lambda(lambda x: x/127.5 - 1.)(x) # normalize and re-center
    x = Convolution2D(24, (5,5), strides=(2,2), activation='relu', name="conv2d_1")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(32, (5,5), strides=(2,2), activation='relu', name="conv2d_2")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(64, (5,5), strides=(2,2), activation='relu', name="conv2d_3")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(64, (3,3), strides=(1,1), activation='relu', name="conv2d_4")(x)
    x = Dropout(drop)(x)
    x = Convolution2D(64, (3,3), strides=(1,1), activation='relu', name="conv2d_5")(x)
    x = Dropout(drop)(x)
    
    x = Flatten(name='flattened')(x)
    x = Dense(100, activation='relu')(x)
    x = Dropout(drop)(x)
    x = Dense(50, activation='relu')(x)
    x = Dropout(drop)(x)

    out = Dense(1, activation='linear', name='out')(x)
        
    model = Model(inputs=[img_in], outputs=out)
    
    return model
    



def train_model(model, X_train, X_valid, y_train, y_valid):
    checkpoint = ModelCheckpoint('daten/modelle/model-{epoch:03d}.h5',
                                 monitor='val_loss',
                                 verbose=0,
                                 save_best_only=save_best_only,
                                 mode='auto')

    model.compile(optimizer="adam", loss="mse")

    model.fit_generator(batch_generator(data_dir, X_train, y_train, batch_size, True),
        	            steps_per_epoch=len(y_train) // batch_size,
                        epochs=args.nb_epoch,
                        verbose=1,
                        validation_data=batch_generator(data_dir, X_valid, y_valid, batch_size, False),
                        validation_steps=len(y_valid) // batch_size,
                        callbacks=[checkpoint])


def main():

    data = load_data(args)
    model = build_model(args)
    train_model(model, args, *data)

if __name__ == '__main__':
    main()