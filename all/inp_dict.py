""" Обрабатывает файл и создает частотный словарь (частота повторения слова в тексте) """
import os
import re
import pymorphy2
import enchant
from language_check import LanguageTool


def make_dict():
    morph = pymorphy2.MorphAnalyzer()
    #tool=language_check.LanguageTool("ru-RU")
    tool=LanguageTool("ru-RU")
    orf_err,total_words,tonal,stop_word,tonal_words=0,0,0,0,0
    work_file = "D:\\text"
    if os.path.isfile(work_file):
        print('Рабочий файл: ' + work_file)
    # читаем файл
    file = open(work_file, 'r')
    try:
        txt = file.read()
    finally:
        file.close()



    txt.strip("\n")
    matches=tool.check(txt)

    #for i in range(len(matches)):#для проверки работы,показывает ошибки(очень круто)
    #    print(matches[i])

    # выбираем слова через регулярные выражения
    p,p1 = re.compile("([а-яА-Я-']+)"),re.compile("([!?])")
    res,res1 = p.findall(txt),p1.findall(txt)
    c = enchant.Dict("ru_RU")
    # создаем словарь. Ключ-слово, Значение-частота повторения
    lsWord = {}
    #ищем слова
    for key in res:
        #key = key.lower()#если оставить,то имена собственные будут считаться как ошибка
        #ПРОВЕРКИ НИЖЕ ВЫНЕСТИ В ОТЕЛЬНЫЙ МЕТОД
        #******************************************
        # проверка на стоп слова
        tmp1=morph.parse(key)[0]
        # INTJ - междометия, PRCL - частицы, CONJ - союзы, PRED - предикатив (некогда)
        if tmp1.tag.POS=="INTJ" or tmp1.tag.POS=="PRCL" or tmp1.tag.POS=="CONJ" or tmp1.tag.POS=="PRED":
            stop_word+=1
        # проверка на слова COMP - компаратив (лучше,хуже и т.д.!!!СЛОВО "ВЫШЕ" НЕ УЧИТЫВАЕТСЯ!!!)
        if tmp1.tag.POS=="COMP":
            tonal_words+=1
        # проверка на орфографическую правильность
        if c.check(key.normal_form)==False:
            orf_err+=1
            #print(key)#вывод некорректных слов
        #******************************************
        if key in lsWord:
            value = lsWord[key]
            lsWord[key] = value + 1
            total_words+=1
        else:
            lsWord[key] = 1
            total_words+=1
    #ищем "?" и "!"
    for key in res1:
        key = key.lower()
        if key in lsWord:
            value = lsWord[key]
            lsWord[key] = value + 1
            tonal+=1
        else:
            lsWord[key] = 1
            tonal+=1
# создаем список ключей отсортированный по значению словаря lsWord
    sorted_keys = sorted(lsWord, key=lambda x: int(lsWord[x]), reverse=True)
    file = open(work_file + '_dict.csv', 'w')
    morph = pymorphy2.MorphAnalyzer()
    try:
        for key in sorted_keys:
            #преобразование к инфинитиву
            #key.normal_form
            p=morph.parse(key)[0]
            words=p.normal_form
            s = str("{0};{1}\r").format(words, lsWord[key])
            file.write(s)
        print('Результат записан: ' + work_file + '_dict.csv')
    finally:
        file.close()
    return orf_err,total_words,tonal,stop_word,tonal_words,len(matches)