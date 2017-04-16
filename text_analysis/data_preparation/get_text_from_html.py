import re
from os import read

import numpy
import requests

input = open('C:/Users/Администратор/PycharmProjects/analysis_text/text_analysis/train_texts/seo_prepared.txt','r')
seo_texts = input.readlines()
print(seo_texts)
for i in range(len(seo_texts)):
    seo_texts[i] = re.sub("[\n]", "", seo_texts[i])

print(seo_texts[1])
# в seo_texts содержатся url с объявлениями

def make(url):
    response = requests.get('http://' + url + '/')
    # print(response.content.decode('utf-8'))# получили html страницу, теперь ищем блоки resourceSource,в них объявления
    answer = response.content.decode('utf-8')
    # print(re.findall('<p  p>', answer))
    div = re.split('<p', answer)[1:]
    div = numpy.array(div)
    divv = div.copy()
    for i in range(div.size - 1):
        divv[i] = re.split('\t', div[i])[0]
        divv[i] = re.sub('style="font-size:12px;">', "", divv[i])
        divv[i] = re.sub("[^а-яА-ЯёЁa-zA-Z0-9%$.']+", " ", divv[i])
    txt = divv.tolist()
    txt.pop()
    txt.pop()
    txt.pop()
    print(txt)
    return txt

def make_files():
    output = open('C:/Users/Администратор/PycharmProjects/analysis_text/text_analysis/train_texts/ready_txts/texts.txt',
                  'w')
    output_csv = open(
        'C:/Users/Администратор/PycharmProjects/analysis_text/text_analysis/train_texts/ready_txts/traindata.tsv', 'w')
    output_csv.write("id\tsentiment\treview\n")
    for i in range(len(seo_texts) - 1):
        txt = make(seo_texts[i])
        for i in range(len(txt) - 1):
            output.write(txt[i] + '\n')
            output_csv.write(str(i + 1) + "\t" + str(1) + "\t" + txt[i] + "\n")
    output.close()
    output_csv.close()


