import numpy as np
import cv2
import timeit
import warnings
import argparse
import operator
import threading
from spellchecker import SpellChecker
from shop_detector.detector import Detector
from shop_recognizer.recognizer import Recognizer
from shop_recognizer.semantic_detector.word_similarity import WordSimilarity

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

parser = argparse.ArgumentParser(description='Automatic Creation of Map Enrichment Data at Scale Using Street-level Images')
parser.add_argument('--input_image', default='input/test4.jpg', type=str, help='Input image for inference')
parser.add_argument('--labels', default='labels/categories.txt', type=str, help='Classification Labels')

args = parser.parse_args()

global frame2

def drawPred(frame, className, conf, left, top, right, bottom):
    # Draw a bounding box.
    #    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

    label = '%.2f' % conf

    label = '%s:%s' % (className, label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv2.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (0, 0, 255), cv2.FILLED)
    # cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine),    (255, 255, 255), cv.FILLED)
    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)


def execute(shop, frame2, coordinates, categories, recognizer, embeddings):

    try:
        height, width, channel = shop.shape
        if (width > 50 and height > 50):
            bow = recognizer.recognize(shop)  # Retrieving bag of words

            tmp = embeddings.checkSemanticSimilarity2(categories, bow)
            tmp = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)
            labelName = tmp[0][0]
            labelConf = tmp[0][1]
            drawPred(frame2, labelName, labelConf, coordinates[0], coordinates[1], coordinates[2], coordinates[3])
    except Exception as e:
        print(e)


if __name__ == '__main__':

    outputFile = "output/final.mp4"
    cap = cv2.VideoCapture("input/test.mp4")

    vid_writer = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc(*'MP4V'), 30,
                                 (round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    # loading detector and recognizer
    detector = Detector(608, 608, 0.3, 0.4)
    recognizer = Recognizer()
    spellchecker = SpellChecker()
    embeddings = WordSimilarity(spellchecker)

    # loading labels
    labels = np.loadtxt(args.labels, str, delimiter='\t')
    categories = []
    for label in labels:
        categories.append(str(label.split(',')[0]))

    start = timeit.default_timer()

    while True:

        # get frame from the video
        hasFrame, frame = cap.read()

        frame2 = frame

        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            print("Output file is stored as ", outputFile)
            cv2.waitKey(3000)
            break

        try:
            index = 0
            result = {}
            shops, coordinates = detector.detect(frame)
            for shop in shops:
                x = threading.Thread(target=execute,
                                     args=(shop, frame2, coordinates[index], categories, recognizer, embeddings))
                x.start()
                x.join()
                index = index + 1

        except Exception as e:
            print(e)

        vid_writer.write(frame2.astype(np.uint8))

    stop = timeit.default_timer()
    print("video has been created...")
    print('Inference time: ', stop - start)
