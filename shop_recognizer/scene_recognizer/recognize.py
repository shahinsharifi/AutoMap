import argparse
import imutils
import cv2
import os
import numpy as np
import operator

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


labels_file = 'labels/categories_places365.txt'
labels = np.loadtxt(labels_file, str, delimiter='\t')

sub_labels_file = 'labels/categories_places365.txt'
sub_labels = np.loadtxt(sub_labels_file, str, delimiter='\t')


# load our serialized face detector from disk
print("[INFO] loading scene recognizer...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"], "weights.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


# load the image, resize it to have a width of 600 pixels (while
# maintaining the aspect ratio), and then grab the image dimensions
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)

# construct a blob from the image
imageBlob = cv2.dnn.blobFromImage(image, 1.0, (224, 224), (104.0, 177.0, 123.0), swapRB=False, crop=False)

# apply OpenCV's deep learning-based face detector to localize
# faces in the input image
detector.setInput(imageBlob)
output = detector.forward(getOutputsNames(detector))

output_prob = output[0][0]
top_inds = output_prob.argsort()


subClass = []
for sbl in sub_labels:
	subClass.append(str(sbl.split(' ')[0]))

print("Getting visual features...")

visulaScores = {}
totalVisualScore = 0
for iterating_var in top_inds:
	className = labels[iterating_var].split(' ')[0]
	if className in subClass:
		score = float(output_prob[iterating_var])
		visulaScores[className] = score
		totalVisualScore = score + totalVisualScore

for tmp in subClass:
	tempScore = float(visulaScores[tmp]) / float(totalVisualScore)
	visulaScores[tmp] = tempScore

visulaScores = sorted(visulaScores.items(), key=operator.itemgetter(1), reverse=True)
visulaScores = visulaScores[0:5]

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)