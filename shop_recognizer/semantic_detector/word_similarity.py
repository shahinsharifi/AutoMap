# -*- coding: utf-8 -*-
import spacy
import numpy as np
import pkg_resources
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

class WordSimilarity:

    def __init__(self, spell):
        max_edit_distance_dictionary = 2
        prefix_length = 7
        self.sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
        dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
        bigram_path = pkg_resources.resource_filename("symspellpy", "frequency_bigramdictionary_en_243_342.txt")
        if not self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
            print("Dictionary file not found")
            return
        if not self.sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2):
            print("Bigram dictionary file not found")
            return

        self.nlp = spacy.load("shop_recognizer/semantic_detector/models/en_core_web_lg")
        self.spell = spell


    def checkSemanticSimilarity2(self, labels, words):
        result = {}
        texts = self.removeNoise2(words)
        for label in labels:
            tmp = ""
            doc1 = self.nlp(label)
            for text in texts:
                tmp += text + " "
            doc2 = self.nlp(tmp)
            score = doc2.similarity(doc1)
            result[label] = int(score * 100)
        prob = self.softmax(labels, result)
        counter = 0
        for cls in labels:
            if len(words):
                result[cls] = float(prob[counter])
                counter = counter + 1
            else:
                result[cls] = 0
        return result


    def checkSemanticSimilarity(self, labels, words):
        result = {}
        texts = self.removeNoise2(words)
        print(texts)
        for label in labels:
            tmp = 0
            doc1 = self.nlp(label)
            for text in texts:
                doc2 = self.nlp(text)
                similarity = doc2.similarity(doc1)
                if similarity > tmp:
                    tmp = similarity
            result[label] = int(tmp * 100)
        prob = self.softmax(labels, result)
        counter = 0
        for cls in labels:
            if len(words):
                result[cls] = float(prob[counter])
                counter = counter + 1
            else:
                result[cls] = 0
        return result


    def removeNoise(self, words):
       result = []
       for word in words:
           if len(word) > 2 and (word.isdigit() is False):
               if(word in self.nlp.Defaults.stop_words):
                   continue
               else:
                   newWord = self.spell.correction(word)
                   if self.nlp.vocab.has_vector(newWord):
                       result.append(newWord)
       return result



    def removeNoise2(self, words):
       result = []
       for word in words:
           if len(word) > 2 and (word.isdigit() is False):
               newWord = self.correct(word)
               newWord = newWord.replace(" ", "")
               result.append(newWord)
       return result



    def correct(self, word):
        input_term = (word)
        max_edit_distance_lookup = 2
        suggestions = self.sym_spell.lookup_compound(input_term, max_edit_distance_lookup)
        return suggestions[0].term


    def softmax(self, classes, scores):
        inputArry = []
        for cls in classes:
            inputArry.append(scores[cls])
        ex = np.exp(inputArry)
        sum_ex = np.sum(np.exp(inputArry))
        return ex / sum_ex
