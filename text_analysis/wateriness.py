import pymorphy2


class Water:

    def __init__(self, obj):
        self.__value = 0.0
        self.__stop_word = 0
        self.__obj = obj
        self.__vocab = obj.get_lsWord()
        self.__wateri(obj)

    def __wateri(self, obj):
        morph = pymorphy2.MorphAnalyzer()
        for key in self.__vocab:
            tmp1 = morph.parse(key)[0]
            if tmp1.tag.POS == "INTJ" or tmp1.tag.POS == "PRCL" or tmp1.tag.POS == "CONJ" or tmp1.tag.POS == "PRED":
                self.__stop_word += 1
        self.__value = self.__stop_word / obj.get_totalword()

    def get_mark(self):
        return self.__value