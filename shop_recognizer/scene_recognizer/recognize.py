import argparse
import imutils
import cv2
import os
import numpy as np
import operator


class SceneRecognition:

	def __init__(self):
		labels_file = 'labels/places365.txt'
		self.labels = np.loadtxt(labels_file, str, delimiter='\t')

		sub_labels_file = 'labels/places22.txt'
		self.sub_labels = np.loadtxt(sub_labels_file, str, delimiter='\t')

		# load our serialized face detector from disk
		print("[INFO] loading scene recognizer...")
		protoPath = "shop_recognizer/scene_recognizer/models/resnet152/deploy.prototxt"
		modelPath = "shop_recognizer/scene_recognizer/models/resnet152/weights.caffemodel"
		self.detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	def detect(self, image):

		# load the image, resize it to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image dimensions
		image = imutils.resize(image, width=600)

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(image, 1.0, (224, 224), (104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		self.detector.setInput(imageBlob)
		output = self.detector.forward(self.getOutputsNames(self.detector))

		output_prob = output[0][0]
		top_inds = output_prob.argsort()

		subClass = []
		for sbl in self.sub_labels:
			subClass.append(str(sbl.split(' ')[0]))

		visulaScores = {}
		totalVisualScore = 0
		for iterating_var in top_inds:
			className = self.labels[iterating_var].split(' ')[0]
			if className in subClass:
				score = float(output_prob[iterating_var])
				visulaScores[className] = score
				totalVisualScore = score + totalVisualScore

		for tmp in subClass:
			tempScore = 0
			if tmp in visulaScores:
				tempScore = float(visulaScores[tmp]) / float(totalVisualScore)
			visulaScores[tmp] = tempScore

		visulaScores = sorted(visulaScores.items(), key=operator.itemgetter(1), reverse=True)
		#visulaScores = visulaScores[0:5]

		return visulaScores


	def getOutputsNames(self, net):
		# Get the names of all the layers in the network
		layersNames = net.getLayerNames()
		# Get the names of the output layers, i.e. the layers with unconnected outputs
		return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

