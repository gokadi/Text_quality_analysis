import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk.data
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import logging
from gensim.models import word2vec


class Word2VecTrain:
    # Параметры Word2Vec модели
    __num_features = 200  # Размерность вектора
    __min_word_count = 40  # Слово, встречающееся меньше этого числа не учитывать. (Фильтрует, например, инициалы)
    __num_workers = 4  # Число параллельных процессов, для ускорения обучения
    __context = 10  # Как много слов из окружения слова должно учитываться при обучении
    __downsampling = 1e-3  # Исключаем часто встречающиеся в тексте слова

    train = pd.read_csv("D:/учеба_магистратура/6курс/Александров/нейросеть/labeledTrainData_RU.tsv", header=0,
                        delimiter="\t", quoting=3)
    test = pd.read_csv("D:/учеба_магистратура/6курс/Александров/нейросеть/testData_RU.tsv", header=0, delimiter="\t",
                       quoting=3)
    unlabeled_train = pd.read_csv("D:/учеба_магистратура/6курс/Александров/нейросеть/unlabeledTrainData_RU.tsv",
                                  header=0, delimiter="\t", quoting=3)
    # Инициализация tokenizer
    __tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    def __init__(self):
        # Verify the number of reviews that were read (100,000 in total)
        print("Read %d labeled train reviews, %d labeled test reviews, "
              "and %d unlabeled reviews" % (
                  self.train["review"].size, self.test["review"].size, self.unlabeled_train["review"].size))
        print("Training model...")
        sentences = self.__make_sentences()
        self.__model = word2vec.Word2Vec(sentences, workers=self.__num_workers,
                                         size=self.__num_features, min_count=self.__min_word_count,
                                         window=self.__context, sample=self.__downsampling)
        # Уменьшает количество используемой RAM
        #self.__model.init_sims(replace=True)
        # Сохраняем модель
        model_name = "300features_40minwords_10context_RU"
        self.__model.save(model_name)

    def __make_sentences(self):
        sentences = []
        print("Parsing sentences from training set")
        for review in self.train["review"]:
            sentences += self.__review_to_sentences(review, self.__tokenizer)
        print("Parsing sentences from unlabeled set")
        for review in self.unlabeled_train["review"]:
            sentences += self.__review_to_sentences(review, self.__tokenizer)  # если делать append, то только первый из
            # списков прикрепится. (list of lists)
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                            level=logging.INFO)
        return sentences

    @staticmethod
    def review_to_wordlist(review, remove_stopwords=False, language="RU"):
        # Делим преложение на список слов (list of words)
        # 1. Очистка от html тегов и URLов
        review = re.sub(r'^https?:\/\/.*[\r\n]*', '', review, flags=re.MULTILINE)
        review_text = BeautifulSoup(review, "html.parser").get_text()
        # 2. Оставить только буквы
        if language == "EN":
            review_text = re.sub("[^a-zA-Z]", " ", review_text)
        elif language == "RU":
            review_text = re.sub("[^а-яА-Я]", " ", review_text)
        # 3. Привести текст к нижнему регистру и разделить на слова
        words = review_text.lower().split()
        # 4. Удалить стоп слова (по флагу)
        if remove_stopwords:
            # stops = set(stopwords.words("english"))
            stops = set(stopwords.words("russian"))
            words = [w for w in words if not w in stops]
        # 5. Вернуть список слов
        return (words)

    def __review_to_sentences(self, review, tokenizer, remove_stopwords=False):
        # Делим обзор на предложения. Обзор - > список предложений - > список слов
        # 1. Используем токенайзер для деления обзора на предложения
        #raw_sentences = tokenizer.tokenize(review.strip())#для английского
        raw_sentences = sent_tokenize(review)
        # 2. Для каждого предложения вызываем функцию преобразования в список слов
        sentences = []
        for raw_sentence in raw_sentences:
            # Пустые предложения пропускаем
            if len(raw_sentence) > 0:
                sentences.append(self.review_to_wordlist(raw_sentence, remove_stopwords))
        # Возвращаем список предложений, каждое из которых - список слов. list of lists
        #print(sentences)
        return sentences
