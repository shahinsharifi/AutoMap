import numpy as np
import cv2
import timeit
import warnings
import argparse
from spellchecker import SpellChecker
from shop_detector.detector import Detector
from shop_recognizer.recognizer import Recognizer
from shop_recognizer.semantic_detector.word_similarity import WordSimilarity

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

parser = argparse.ArgumentParser(description='Automatic Creation of Map Enrichment Data at Scale Using Street-level Images')
parser.add_argument('--input_image', default='input/sample3.jpg', type=str, help='Input image for inference')
parser.add_argument('--labels', default='labels/categories.txt', type=str, help='Classification Labels')

args = parser.parse_args()


if __name__ == '__main__':

    # loading detector and recognizer
    detector = Detector(608, 608, 0.3, 0.4)
    recognizer = Recognizer()
    #spellchecker = SpellChecker()
    #embeddings = WordSimilarity(spellchecker)

    # loading labels
    labels = np.loadtxt(args.labels, str, delimiter='\t')
    categories = []
    for label in labels:
        categories.append(str(label.split(' ')[0]))

    start = timeit.default_timer()

    index = 1
    result = {}
    shops, coordinates = detector.detect(args.input_image)
    for shop in shops:
        cv2.imwrite('output/shop' + str(index) + '.jpg', shop)
        bow = recognizer.recognize(shop)  # Retrieving bag of words

       #categoryRanks = embeddings.checkSemanticSimilarity(categories, bow)
       #categoryRanks = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)

        result['shop' + str(index)] = bow
        index = index + 1

    stop = timeit.default_timer()

    print('Inference time: ', stop - start)
    print(result)
    print(coordinates)