from shop_recognizer.scene_text_detector.text_detection import TextDetection
from shop_recognizer.scene_recognizer.recognize import SceneRecognition
import cv2

class Recognizer:

	def __init__(self):
		# Loading text detection network
		self.sceneRecognition = SceneRecognition()
		self.textDet = TextDetection()

	def recognize(self, image):
		#image = cv2.imread(inputImage)
		recognition = self.sceneRecognition.detect(image)
		detection = self.textDet.detect(image)
		return detection, recognition
