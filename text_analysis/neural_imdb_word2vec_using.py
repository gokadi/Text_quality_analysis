from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from text_analysis.neural_imdb_word2vec_training import Word2VecTrain
from sklearn.externals import joblib


class Word2VecUsage:
    __num_features = int(200)  # Размерность вектора слов

    def __init__(self):
        self.train = Word2VecTrain.train
        self.test = Word2VecTrain.test
        self.__model = Word2Vec.load("300features_40minwords_10context_RU")
        self.__forest_train()
        joblib.dump(self.__forest,'randomforestTRAINED.pkl')# сохраняем обученный классификатор
        # self.__forest = joblib.load('randomforestTRAINED.pkl')
        # self.__forest_test()

    def pred(self, txt):
        return self.__forest.predict(
            self.__makeFeatureVec(Word2VecTrain.review_to_wordlist(txt), self.__model, self.__num_features))

    def __forest_test(self):
        # Test & extract results
        result = self.__forest.predict(self.__test_reviews())
        # Write the test results
        output = pd.DataFrame(data={"id": self.test["id"], "sentiment": result})
        output.to_csv("D:/учеба_магистратура/6курс/Александров/нейросеть/Word2Vec_AverageVectors_RU.tsv", index=False,
                      sep="\t", quoting=3)

    def __forest_train(self):
        self.__forest = RandomForestClassifier(n_estimators=100)  # Число деревьев
        print("Fitting a random forest to labeled training data...")
        self.__forest = self.__forest.fit(self.__train_reviews(), self.train["sentiment"])

    def __test_reviews(self):
        print("Creating average feature vecs for test reviews")
        clean_test_reviews = []
        for review in self.test["review"]:
            clean_test_reviews.append(Word2VecTrain.review_to_wordlist(review,
                                                                       remove_stopwords=True))
        # self.testDataVecs = self.__getAvgFeatureVecs(clean_test_reviews, self.__model, self.__num_features)
        return self.__getAvgFeatureVecs(clean_test_reviews, self.__model, self.__num_features)

    def __train_reviews(self):
        print("Creating average feature vecs for train reviews")
        clean_train_reviews = []
        for review in self.train["review"]:
            clean_train_reviews.append(Word2VecTrain.review_to_wordlist(review,
                                                                        remove_stopwords=True))
        # self.trainDataVecs = self.__getAvgFeatureVecs(clean_train_reviews, self.__model, self.__num_features)
        return self.__getAvgFeatureVecs(clean_train_reviews, self.__model, self.__num_features)

    # в модели просто вектора для всех слов из всех обзоров.
    # здесь для каждого обзора составляем усредненный вектор
    def __makeFeatureVec(self, words, model, num_features):
        # Усредняем вектора для всех слов в обзоре
        # Инициализируем массив
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0.
        # Index2word - список, содержащий слова из словаря модели. Конвертируем в set
        index2word_set = set(model.wv.index2word)
        # Для всех слова в обзоре, если они в словаре, суммируем вектора
        for word in words:
            if word in index2word_set:
                nwords = nwords + 1.
                featureVec = np.add(featureVec, model[word])
        # Усредняем получившийся вектор
        featureVec = np.divide(featureVec, nwords)
        return featureVec

    def __getAvgFeatureVecs(self, reviews, model, num_features):
        # Вычисляем усредненные вектора для набора обзоров
        # Инициализируем счетчик
        counter = int(0)
        # Инициализация массива усредненных векторов
        reviewFeatureVecs = np.zeros((len(reviews), num_features), dtype="float32")
        # Цикл по всем обзорам
        for review in reviews:
            # Статус вычислений
            if counter % 1000. == 0.:
                print("Review %i of %d" % (counter, len(reviews)))
            # Для каждого обзора вычисляем его усредненный вектор
            reviewFeatureVecs[counter] = self.__makeFeatureVec(review, model,
                                                               num_features)
            # Счетчик ++
            counter = counter + 1
        # Возвращаем массив усредненных векторов
        return reviewFeatureVecs
