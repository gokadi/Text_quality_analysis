from collections import OrderedDict
import pymorphy2


class Tonal:

    def __init__(self, obj):
        self.__value = 0.0
        self.__obj = obj
        self.__vocab = obj.get_lsWord() # словарь без предлогов, междометий, местоимений и тд
        self.__clear(obj)

    def __clear(self, obj):
        morph = pymorphy2.MorphAnalyzer()
        cr = {}
        for key in self.__vocab:
            tmp1 = morph.parse(key)[0]
            if not (tmp1.tag.POS == "INTJ" or tmp1.tag.POS == "PRCL" or tmp1.tag.POS == "CONJ"
                    or tmp1.tag.POS == "PRED" or key == "?" or key == "!" or tmp1.tag.POS == "PREP"
                    or tmp1.tag.POS == "NUMR" or tmp1.tag.POS == "NPRO"):
                cr[tmp1] = self.__vocab[key]
        self.__vocab = OrderedDict(sorted(cr.items()))

    def get_mark(self):
        return 1 - self.__value

