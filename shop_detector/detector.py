import cv2 as cv
import numpy as np


class Detector:

    def __init__(self, inpWidth, inpHeight, confThreshold, nmsThreshold):

        # Initialize the parameters
        self.confThreshold = confThreshold  # Confidence threshold
        self.nmsThreshold = nmsThreshold  # Non-maximum suppression threshold

        self.inpWidth = inpWidth  # Width of network's input image
        self.inpHeight = inpHeight  # Height of network's input image

        # Load names of classes
        classes = None
        classesFile = "shop_detector/models/classes.names"
        with open(classesFile, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
        self.classes = classes

        # Give the configuration and weight files for the model and load the network using them.
        modelConfig = "shop_detector/models/yolo.cfg"
        modelWeights = "shop_detector/models/shop.weights"
        
        self.net = cv.dnn.readNetFromDarknet(modelConfig, modelWeights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)



    # Get the names of the output layers
    def getOutputsNames(self, net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


    # Crop and return the predicted bounding box
    def extractResult(self, frame, left, top, right, bottom):
        box = frame[top:bottom, left:right, :]
        return box

    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(self, frame, outs):

        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)

                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        result = []
        coordinates = []
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            coordinates.append((box[0], box[1], box[0]+box[2], box[1]+box[3]))
            box = self.extractResult(frame, left, top, left + width, top + height)
            result.append(box)

        return result, coordinates


    def detect(self, inputImage):

        cap = cv.VideoCapture(inputImage)

        # get frame from the video
        hasFrame, frame = cap.read()

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        self.net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.getOutputsNames(self.net))

        # Remove the bounding boxes with low confidence
        result, coordinates = self.postprocess(frame, outs)

        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()

     #   logs = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())

      #  print(logs)

        return result, coordinates

