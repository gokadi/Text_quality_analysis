from nltk.corpus import sentiwordnet as swn
import pymorphy2


class Tonal:
    __pos = 0
    __neg = 0
    __ob = 0

    def __init__(self, obj):
        self.__orf_err = 0
        self.__value = 0.0
        self.__obj = obj
        self.__vocab = obj.get_words()
        self.__toni(obj)

    def __toni(self, obj):
        morph = pymorphy2.MorphAnalyzer()
        for key in self.__vocab:
            tmp1 = morph.parse(key)[0].normal_form
            print(tmp1)
            self.__pos += swn.senti_synset(tmp1).pos_score()
            self.__neg += swn.senti_synset(tmp1).pos_score()
            self.__ob += swn.senti_synset(tmp1).obj_score()
        print(self.__pos," ",self.__neg," ",self.__ob)

    def get_mark(self):
        return 1 - self.__value