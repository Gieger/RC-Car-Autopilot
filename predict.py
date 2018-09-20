import cv2, os
import numpy as np
import matplotlib.image as mpimg
import glob
from PIL import Image
from keras.models import load_model
import utils






IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)


filelist = glob.glob("C:/Users/Tron/Desktop/Herbie/Data/Image2/*.jpg")

print("Load Model")
model = load_model('Data/Model/model-008.h5')
print("Model bereit")

for fname in filelist:
    image = mpimg.imread(fname)
    

    #__image2 = cv2.cvtColor(__image1, cv2.COLOR_BGR2RGB) 

    __image1 = utils.preprocess(image)
    __image2 = np.asarray(__image1, dtype=np.float32)
    __image = np.array([__image2]) 

    cv2.imshow('image',__image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows          

    __steering_angle = model.predict(__image, batch_size=1)
    steer = __steering_angle[0][0]
    throt = __steering_angle[0][1]
    throt = throt * -1
    if steer < -1:
        steer = -1
    if steer > 1:
        steer = 1
    

    #steer = int(steer * 120)
    print ("Lenken ------------------")
    print(steer)

                