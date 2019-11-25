# -*- coding: utf-8 -*-
import spacy
import numpy as np

class WordSimilarity:

    def __init__(self, spell):
        # https://spacy.io/models/en
        self.model = spacy.load('en_vectors_web_lg')
        self.spell = spell


    def checkSemanticSimilarity(self, labels, words):
        result = {}
        totalTextualScore = 0
        words = self.removeNoise(words)
        for label in labels:
            tmpSimilarity = 0
            for word in words:
                if (label in self.model.vocab):
                        vLabel = self.model.vocab[label]
                        vNewWord = self.model.vocab[word]
                        similarity = vNewWord.similarity(vLabel)
                        if similarity > tmpSimilarity:
                            tmpSimilarity = similarity
            result[label] = int(tmpSimilarity * 100)
            totalTextualScore = tmpSimilarity + totalTextualScore
        softM = self.softmax(labels, result)
        counter = 0
        for cls in labels:
            if len(words):
                result[cls] = float(softM[counter])
                counter = counter + 1
            else:
                result[cls] = 0
        return result


    def removeNoise(self, words):
       result = []
       for word in words:
           if len(word) > 2 and (word.isdigit() is False):
               if(word in self.model.Defaults.stop_words):
                    continue
               else:
                    newWord = self.spell.correction(word)
                    if (newWord in self.model.vocab):
                        result.append(newWord)
       return result


    def softmax(self, classes, scores):
        inputArry = []
        for cls in classes:
            inputArry.append(scores[cls])
        ex = np.exp(inputArry)
        sum_ex = np.sum(np.exp(inputArry))
        return ex / sum_ex
