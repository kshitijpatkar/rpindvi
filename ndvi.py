import cv2
import numpy as np
from fastiecm import fastiecm
from picamera import PiCamera
import picamera.array
from time import sleep
from os import mkdir, chdir

chdir(images)
name = input("Enter name: ")
mkdir(name)
chdir(name)

cam = PiCamera()
cam.rotation = 270
cam.resolution = (1920, 1080)

stream = picamera.array.PiRGBArray(cam)
cam.start_preview()
sleep(5)
cam.capture(stream, format='bgr', use_video_port=True)
cam.stop_preview()
original = stream.array

def display(image, image_name):
    image = np.array(image, dtype=float)/float(255) # convert to an array

    shape = image.shape
    height = int(shape[0]/2)
    width = int(shape[1]/2)
    image = cv2.resize(image, (width, height))

    cv2.namedWindow(image_name) # create window
    cv2.imshow(image_name, image) # display image
    cv2.waitKey(0) # wait for keypress
    cv2.destroyAllWindows()

def contrast_stretch(im):
    in_min = np.percentile(im, 5) # find bottom 5 percentile
    in_max = np.percentile(im, 95) # find top 5 percentile

    out_min = 0.0
    out_max = 255.0

    # stretch out values
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (r.astype(float) - b) / bottom
    return ndvi


display(original, 'Original')
cv2.imwrite('1_original.png', original)

contrasted = contrast_stretch(original)
display(contrasted, 'Contrasted original')
cv2.imwrite('2_contrasted.png', contrasted)

ndvi = calc_ndvi(contrasted)
display(ndvi, 'NDVI')
cv2.imwrite('3_ndvi.png', ndvi)

ndvi_contrasted = contrast_stretch(ndvi)
display(ndvi_contrasted, 'NDVI Contrasted')
cv2.imwrite('4_ndvi_contrasted.png', ndvi_contrasted)

colour_mapped_prep = ndvi_contrasted.astype(np.uint8)
colour_mapped_image = cv2.applyColorMap(colour_mapped_prep, fastiecm)
display(colour_mapped_image, 'Colour mapped')
cv2.imwrite('5_colour_mapped_image.png', colour_mapped_image)
