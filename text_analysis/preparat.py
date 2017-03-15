import os
import re
import pymorphy2
import enchant
from language_check import LanguageTool
from collections import OrderedDict


class PrepText:

    def __init__(self, work_file):
        self.__total_words = 0
        self.__work_file = ""
        self.__file = ""
        self.__tool = LanguageTool("ru-RU")
        self.__ch = enchant.Dict("ru_RU")
        self.__morph = pymorphy2.MorphAnalyzer()
        self.__lsWord = {}
        self.__txt = ""
        self.__work_file = work_file
        self.__dict_file = open(self.__work_file + '_dict.csv', 'w')
        self.__read_file()
        self.__make_dict()

    def __read_file(self):
        if os.path.isfile(self.__work_file):
            print('Рабочий файл: ' + self.__work_file + '.')
            # читаем файл
            file = open(self.__work_file, 'r')
            try:
                self.__txt = file.read()
            except:
                print('Непредвиденная ошибка при чтении файла.')
            finally:
                file.close()
        else:
            print('Указанного файла нет!')

    def __make_dict(self):
        self.__txt.strip("\n")
        # выбираем слова через регулярные выражения
        p, p1 = re.compile("([а-яА-Я-']+)"), re.compile("([!?])")
        res, res1 = p.findall(self.__txt), p1.findall(self.__txt)
        # создаем словарь. Ключ-слово, Значение-частота повторения
        # ищем слова
        for key in res:
            if key in self.__lsWord:
                value = self.__lsWord[key]
                self.__lsWord[key] = value + 1
                self.__total_words += 1
            else:
                self.__lsWord[key] = 1
                self.__total_words += 1
        # ищем "?" и "!"
        for key in res1:
            key = key.lower()
            if key in self.__lsWord:
                value = self.__lsWord[key]
                self.__lsWord[key] = value + 1
            else:
                self.__lsWord[key] = 1
        self.__normalform()
        try:
            self.__dict_file = open(self.__work_file + '_dict.csv', 'w')
            for key in self.__lsWord:
                s = str("{0};{1}\r").format(key, self.__lsWord[key])
                self.__dict_file.write(s)
            print('Результат записан: ' + self.__work_file + '_dict.csv')
        except:
            print('Ошибка записи частноного словаря в файл.')
        finally:
            self.__dict_file.close()

    def __normalform(self):
        cr = {}
        for key in self.__lsWord:
            words = self.__morph.parse(key)[0].normal_form
            cr[words] = self.__lsWord[key]
        self.__lsWord = OrderedDict(sorted(cr.items()))

    def get_lsWord(self):
        return self.__lsWord