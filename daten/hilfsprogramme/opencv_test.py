import cv2, os
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import glob
from PIL import Image
from keras.models import load_model
import utils
import time
print("Load Model")
model = load_model('Data/model.h5')
print("Model bereit")







data_df = pd.read_csv(os.path.join(os.getcwd(), 'Data/Log', 'driving_log.csv'), names=['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed'])

X = data_df['center'].values
y = data_df['steering'].values
i=0
shape=y.shape[0]
print(shape)
while i <= shape:
    time.sleep(0.1)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (0,160)
    fontScale              = 1
    fontColor              = (0,255,0)
    lineType               = 2
    d = X[i]
    e = y[i]
    img = mpimg.imread(d)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    __image1 = utils.preprocess(img)
    __image2 = np.asarray(__image1, dtype=np.float32)
    __image = np.array([__image2]) 
    __steering_angle = float(model.predict(__image, batch_size=1))
    __steering_angle = round(__steering_angle, 2)


    cv2.putText(img,str(e), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)


    e = int(e * 120) 

    cv2.line(img,(160 + e,80),(160,160),(0,255,0),2)


    fontColor              = (0,0,255)
    bottomLeftCornerOfText = (0,120)

    cv2.putText(img,str(__steering_angle), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    __steering_angle = int(__steering_angle * 120)
    cv2.line(img,(160 + __steering_angle,80),(160,160),(0,0,255),2)
    
    cv2.imwrite("Data/Imagetext/"+ str(i) + ".jpg", img)
    #cv2.imshow('image',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows
    
    i = i+1







"""
IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS = 66, 200, 3
INPUT_SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS)

i=0

          # Simple brightness control

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)    

filelist = glob.glob("/home/ocp/Schreibtisch/Herbie/Data/Image/*.jpg")
for fname in filelist:
    img = mpimg.imread(fname)
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img1, cv2.COLOR_RGB2YUV)

    gamma = 0.5                                   # change the value here to get different result
    adjusted = adjust_gamma(img, gamma=gamma)
    

    
    img3 = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
    img4 = cv2.cvtColor(img3, cv2.COLOR_RGB2YUV)
    #img1=random_brightness(img1)
    crop = img4[20:380, :, :]
    crop1 = cv2.resize(crop, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_AREA)
    #cv2.imwrite("data/crop/crop_" + str(i) + ".jpg" , crop)
    yuv = cv2.cvtColor(crop1, cv2.COLOR_RGB2YUV)
    #cv2.imwrite("data/yuv/yuv_" + str(i) + ".jpg", yuv)
    #gray_image = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    #blurred_image = cv2.GaussianBlur(crop, (99, 99), 0)
    #blur = cv2.blur(crop,(9,9))
    #blur = cv2.bilateralFilter(crop,59,175,175)s
    #edges_image = cv2.Canny(blurred_image, 50, 120)
    #yuv1 = cv2.cvtColor(blurred_image, cv2.COLOR_RGB2YUV)
    #yuv2 = cv2.cvtColor(blur, cv2.COLOR_RGB2YUV)
    #cv2.imwrite("data/edges/edges_" + str(i) + ".jpg", edges_image)


    cv2.imshow('image3',img3)
    cv2.imshow('image1',img4)
    cv2.imshow('image2',img1)
    cv2.imshow('image4',img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows
    i = i + 1


    #cv2.imwrite("test_neu.jpg", y)
"""


