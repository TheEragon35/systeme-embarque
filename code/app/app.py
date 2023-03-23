import torch
import matplotlib.pyplot as plt
import depthai as dai
import shutil
import os
import cv2
import numpy as np


class Model():
    
    def __init__(self):
        pass

    def loadModel(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def prediction(self, im):
        return self.model(im)

class Camera:
    def __init__(self):
        pass

    def setup(self):
        # Create pipeline
        self.pipeline = dai.Pipeline()

        # Define source and output
        self.camRgb = self.pipeline.create(dai.node.ColorCamera)
        self.xoutRgb = self.pipeline.create(dai.node.XLinkOut)

        self.xoutRgb.setStreamName("rgb")

        # Properties
        self.camRgb.setPreviewSize(640, 640)
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

        # Linking
        self.camRgb.preview.link(self.xoutRgb.input)
    
    def printInformation(self, deviceCamera):
        print('Connected cameras:', deviceCamera.getConnectedCameraFeatures())
        # Print out usb speed
        print('Usb speed:', deviceCamera.getUsbSpeed().name)
        # Bootloader version
        if deviceCamera.getBootloaderVersion() is not None:
            print('Bootloader version:', deviceCamera.getBootloaderVersion())
        # Device name
        print('Device name:', deviceCamera.getDeviceName())
    

if __name__ == "__main__":
    model = Model()
    model.loadModel()

    camera = Camera()
    camera.setup()

    # Connect to device and start pipeline
    with dai.Device(camera.pipeline) as deviceCamera:

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = deviceCamera.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            orig_image = inRgb.getCvFrame() #store frame

            results = model.prediction(orig_image)

            # Show
            cv2.imshow("YOLOv7 Pose Estimation Demo", results.render()[0])
            cv2.waitKey(1)  # 1 millisecond