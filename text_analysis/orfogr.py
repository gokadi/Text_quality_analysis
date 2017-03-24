import enchant
import pymorphy2


class Orthography:

    def __init__(self, obj):
        self.__orf_err = 0
        self.__value = 0.0
        self.__obj = obj
        self.__vocab = obj.get_words()
        self.__wateri(obj)

    def __wateri(self, obj):
        morph = pymorphy2.MorphAnalyzer()
        c = enchant.Dict("ru_RU")
        for key in self.__vocab:
            tmp1 = morph.parse(key)[0]
            if c.check(tmp1.normal_form) == False:
                self.__orf_err += 1
        self.__value = self.__orf_err/ obj.get_totalword()
        if self.__value >= 0.5:
            self.__value = 1.0
        else:
            self.__value *= 2

    def get_mark(self):
        return 1 - self.__value