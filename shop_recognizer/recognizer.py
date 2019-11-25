from shop_recognizer.scene_text_detector.text_detection import TextDetection
import cv2

class Recognizer:

	def __init__(self):
		# Loading text detection network
		self.textDet = TextDetection()

	def recognize(self, image):
		#image = cv2.imread(inputImage)
		detection = self.textDet.detect(image)
		return detection