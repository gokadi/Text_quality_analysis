import pymorphy2
from nltk.corpus import stopwords
import nltk

class Water:

    def __init__(self, obj):
        self.__value = 0.0
        self.__stop_word = 0
        self.__obj = obj
        self.__vocab = obj.get_words()
        self.__wateri(obj)

    def __wateri(self, obj):
        morph = pymorphy2.MorphAnalyzer()
        for key in self.__vocab:
            tmp1 = morph.parse(key)[0]
            if tmp1.tag.POS == "INTJ" or tmp1.tag.POS == "PRCL" or tmp1.tag.POS == "CONJ" or tmp1.tag.POS == "PRED":
                self.__stop_word += 1
        self.__value = self.__stop_word / obj.get_totalword()
        if self.__value >= 0.5:
            self.__value = 1.0
        else:
            self.__value *= 2

    def get_mark(self):
        return 1 - self.__value