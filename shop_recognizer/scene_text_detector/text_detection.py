# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import torch
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from shop_recognizer.scene_text_detector.core import craft_utils
from shop_recognizer.scene_text_detector.core import imgproc
from shop_recognizer.scene_text_detector.core.craft import CRAFT
from shop_recognizer.scene_text_detector.core.refinenet import RefineNet
from shop_recognizer.scene_text_recognizer.text_recognizer import TextRecognizer
from collections import OrderedDict

class TextDetection:

	def __init__(self):

		# Loading initial detection parameters
		self.mainModel = 'shop_recognizer/scene_text_detector/core/model/vgg_plus.pth'
		self.refineModel = 'shop_recognizer/scene_text_detector/core/model/refiner.pth'
		self.textThreshold = 0.7
		self.linkThreshold = 0.4
		self.refinement = False
		self.cuda = False
		self.lowText = 0.4
		self.poly = False
		self.magRatio = 1.5
		self.canvasSize = 1280

		# load net
		net = CRAFT()  # initialize
		print('Loading weights from checkpoint (' + self.mainModel + ')')
		if self.cuda:
			net.load_state_dict(self.copyStateDict(torch.load(self.mainModel)))
		else:
			net.load_state_dict(self.copyStateDict(torch.load(self.mainModel, map_location='cpu')))

		if self.cuda:
			net = net.cuda()
			net = torch.nn.DataParallel(net)
			cudnn.benchmark = False

		net.eval()

		# LinkRefiner
		refine_net = None
		if self.refinement:

			refine_net = RefineNet()
			print('Loading weights of refiner from checkpoint (' + self.refineModel + ')')
			if self.cuda:
				refine_net.load_state_dict(self.copyStateDict(torch.load(self.refineModel)))
				refine_net = refine_net.cuda()
				refine_net = torch.nn.DataParallel(refine_net)
			else:
				refine_net.load_state_dict(self.copyStateDict(torch.load(self.refineModel, map_location='cpu')))

			refine_net.eval()
			self.poly = True

		self.refine_net = refine_net
		self.net = net

		# loading text recognizer network
		self.textRec = TextRecognizer()


	def detect(self, image):

		t = time.time()

		bboxes, polys, score_text = self.test_net(self.net, image, self.textThreshold, self.linkThreshold, self.lowText,
											 self.cuda, self.poly, self.refine_net)

		res = self.saveResult(image, polys)

		return res
	#	print("elapsed time : {}s".format(time.time() - t))


	def test_net(self, net, image, text_threshold, link_threshold, low_text, cuda, poly, refine_net=None):
		t0 = time.time()

		# resize
		img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, self.canvasSize,
																			  interpolation=cv2.INTER_LINEAR,
																			  mag_ratio=self.magRatio)
		ratio_h = ratio_w = 1 / target_ratio

		# preprocessing
		x = imgproc.normalizeMeanVariance(img_resized)
		x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
		x = Variable(x.unsqueeze(0))  # [c, h, w] to [b, c, h, w]

		if cuda:
			x = x.cuda()

		# forward pass
		y, feature = net(x)

		# make score and link map
		score_text = y[0, :, :, 0].cpu().data.numpy()
		score_link = y[0, :, :, 1].cpu().data.numpy()

		# refine link
		if refine_net is not None:
			y_refiner = refine_net(y, feature)
			score_link = y_refiner[0, :, :, 0].cpu().data.numpy()

		t0 = time.time() - t0
		t1 = time.time()

		# Post-processing
		boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

		# coordinate adjustment
		boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
		polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
		for k in range(len(polys)):
			if polys[k] is None: polys[k] = boxes[k]

		t1 = time.time() - t1

		# render results (optional)
		render_img = score_text.copy()
		render_img = np.hstack((render_img, score_link))
		ret_score_text = imgproc.cvt2HeatmapImg(render_img)

	#	print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

	#	crop_img = img[y:y + h, x:x + w]
	#	cv2.imshow("cropped", crop_img)

		return boxes, polys, ret_score_text


	def copyStateDict(self, state_dict):
		if list(state_dict.keys())[0].startswith("module"):
			start_idx = 1
		else:
			start_idx = 0
		new_state_dict = OrderedDict()
		for k, v in state_dict.items():
			name = ".".join(k.split(".")[start_idx:])
			new_state_dict[name] = v
		return new_state_dict


	def saveResult(self, image, boxes):

		# load the input image and grab the image dimensions
		orig = image.copy()
		(origH, origW) = image.shape[:2]

		# set the new width and height and then determine the ratio in change
		# for both the width and height
		(newW, newH) = ((origH, origW))

		rW = origW / float(newW)
		rH = origH / float(newH)

		# initialize the list of results
		results = []
		padding = 0.08
		# loop over the bounding boxes
		index = 0
		for box in boxes:

			startX = int(box[0][0])
			endX = int(box[2][0])
			startY = int(box[0][1])
			endY = int(box[2][1])

			# in order to obtain a better OCR of the text we can potentially
			# apply a bit of padding surrounding the bounding box -- here we
			# are computing the deltas in both the x and y directions
			dX = int((endX - startX) * padding)
			dY = int((endY - startY) * padding)

			# apply padding to each side of the bounding box, respectively
			startX = max(0, startX - dX)
			startY = max(0, startY - dY)
			endX = min(origW, endX + (dX * 2))
			endY = min(origH, endY + (dY * 2))

			# extract the actual padded ROI
			roi = orig[startY:endY, startX:endX]

			img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

			#path, dirs, files = next(os.walk("output"))
			#file_count = len(files)
			#cv2.imwrite('output/'+str(file_count + 1)+'.jpg', roi)
			text = self.textRec.recognize(img)

			# add the bounding box coordinates and OCR'd text to the list
			# of results
			results.append(text)

			index = index + 1
		# sort the results bounding box coordinates from top to bottom
		#results = sorted(results, key=lambda r: r[0][1])
		return results