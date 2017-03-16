import pymorphy2


class Informativity:

    def __init__(self, obj):
        self.__value = 0.0
        self.__stop_word = 0
        self.__obj = obj
        self.__vocab = obj.get_lsWord()
        self.__inf(obj)

    def __inf(self, obj):
        self.__value = len(self.__vocab) / obj.get_totalword()

    def get_mark(self):
        return self.__value