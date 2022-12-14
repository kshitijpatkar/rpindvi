# Measuring plant health

###### Computer Science Impulse

In this project, we are using a [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) and a [Raspberry Pi Camera Module 2 NoIR](https://www.raspberrypi.com/products/pi-noir-camera-v2/) to semi-accurately measure plant health. An [official project](https://projects.raspberrypi.org/en/projects/astropi-ndvi/) was used as a guideline.

![Raspberry Pi with the Pi NoIR Camera Module](/images/rpi.png "Raspberry Pi with the Pi NoIR Camera Module")
_The Raspberry Pi 4B with the Pi NoIR Camera Module_

The Pi is kept in a [case](https://www.raspberrypi.com/products/raspberry-pi-4-case/) which does not have a convenient way of attaching a camera module to the board. The camera is threaded from above one of the USB ports and secured on top of the case using some masking tape, along with the blue-light filter. For convenience, it is only connected to the power, and is accessed remotely using SSH and VNC virtual servers.

The project consists of the following steps:
1. Capturing an image
2. Increasing contrast
3. Calculating NDVI
4. Colour mapping

Although the project is in a usable state, there are still a few quality-of-life improvements which can be made, tracked here:
- [x] Capture image
- [x] Increase contrast
- [x] Calculate NDVI
- [x] Colour map
- [x] Save processed images
- [x] Save images based on input name
- [ ] Overlay colour guide on images (manually?)

It is recommended that the following pages are read:
- [Capture plant health with NDVI and Raspberry Pi](https://projects.raspberrypi.org/en/projects/astropi-ndvi/)
- [What’s that blue thing doing here?](https://www.raspberrypi.com/news/whats-that-blue-thing-doing-here/)

The above pages should ideally inform the reader about how the project works. A few small changes have been made to the given project which are documented below:

### Previewing the image

In the original project, the camera was found to not have enough time to adjust to the light level. As such, a preview is launched for an arbitrary amount of time (the documentation recommends at least 2 seconds, the project uses 5). In addition, this helps take the image since the original project provides no guidance using a preview. The changed code is below.

```python
from picamera import PiCamera
import picamera.array
from time import sleep                         # changed line

cam = PiCamera()
cam.rotation = 270
cam.resolution = (1920, 1080)

stream = picamera.array.PiRGBArray(cam)
cam.start_preview()                            # changed line
sleep(5)                                       # changed line
cam.capture(stream, format='bgr', use_video_port=True)
cam.stop_preview()                             # changed line
original = stream.array
```

### Adjusting for the Pi NoIR Camera

The original project uses a [Raspberry Pi High Quality Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/), which is not an infrared camera, and hence the guide removes the infrared filter on it and installs a red filter. But since we are using Pi NoIR Camera, a blue light filter has been put onto the camera and the code edited to match. The changed code is below.

```python
def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (r.astype(float) - b) / bottom      # changed line
    return ndvi
```

### Saving named images

Since we plan to measure the health of multiple plants, every time the program is run, the user is prompted for a name. A separate directory is created and switched to, in which all the numbered processed images are saved. The important changed code is below.

```python
from time import sleep
from os import mkdir, chdir                    # changed line

chdir(images)                                  # changed line
name = input("Enter name: ")                   # changed line
mkdir(name)                                    # changed line
chdir(name)                                    # changed line
```
