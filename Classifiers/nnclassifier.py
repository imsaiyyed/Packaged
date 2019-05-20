# -*- coding: utf-8 -*-
#Importing required packages
import Configuration.config as config
from keras.engine.saving import load_model
import pickle
from keras_preprocessing import sequence

class SentimentAnalyzer:
    def __init__(self):
        self.nn_classifier = load_model('Learnings/nnClassifier')
        self.maxfeatures=config.NN_MAX_FEATURS
        
        filename = 'Learnings/nn_vectorizer.pkl'
        fileObject = open(filename, 'rb')
        self.nn_vectorizer = pickle.load(fileObject)
    
    def getSentiments(self,text):
        X=self.nn_vectorizer.transform([text]).toarray()
        X = sequence.pad_sequences(X, maxlen=self.maxfeatures)
        proba=self.nn_classifier.predict(X)
        classpred = self.nn_classifier.predict_classes(X)
  
        prediction=(proba[0][0], proba[0][1], proba[0][2], classpred[0])
        return prediction

#sa=SentimentAnalyzer()
#result=sa.getSentiments('I am very happy')