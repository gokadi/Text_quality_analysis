from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from text_analysis.neural_imdb_word2vec_training import Word2VecTrain


class Word2VecUsage:
    __num_features = int(300)  # Размерность вектора слов

    def __init__(self):
        train = Word2VecTrain.train
        test = Word2VecTrain.test
        self.__model = Word2Vec.load("300features_40minwords_10context")

        # ****************************************************************
        # Вызов функций для набора данных

        print("Creating average feature vecs for train reviews")
        clean_train_reviews = []
        for review in train["review"]:
            clean_train_reviews.append(Word2VecTrain.review_to_wordlist(review,
                                                                        remove_stopwords=True))

        trainDataVecs = self.__getAvgFeatureVecs(clean_train_reviews, self.__model, self.__num_features)

        print("Creating average feature vecs for test reviews")
        clean_test_reviews = []
        for review in test["review"]:
            clean_test_reviews.append(Word2VecTrain.review_to_wordlist(review,
                                                                       remove_stopwords=True))

        testDataVecs = self.__getAvgFeatureVecs(clean_test_reviews, self.__model, self.__num_features)

        forest = RandomForestClassifier(n_estimators=100)  # Число деревьев

        print("Fitting a random forest to labeled training data...")
        forest = forest.fit(trainDataVecs, train["sentiment"])

        # Test & extract results
        result = forest.predict(testDataVecs)

        # Write the test results
        output = pd.DataFrame(data={"id": test["id"], "sentiment": result})
        output.to_csv("D:/учеба_магистратура/6курс/Александров/нейросеть/Word2Vec_AverageVectors.tsv", index=False,
                      sep="\t", quoting=3)

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



