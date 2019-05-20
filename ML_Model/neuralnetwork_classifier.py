# -*- coding: utf-8 -*-

# Artificial Neural Network

# import required libraries
from keras import regularizers
from keras_preprocessing import sequence
import pandas as pd
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import nltk
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Embedding
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer,HashingVectorizer
from sklearn.model_selection import train_test_split
# Load dataset
dataset = pd.read_csv('Dataset/review_data.tsv', delimiter = '\t', quoting = 3)
#
#
# import re
# import nltk
#
nltk.download('stopwords')
#
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
#
with open('Dataset/review_data.tsv') as f:
    size=sum(1 for _ in f)

for i in range(0, size-1):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    # b = TextBlob(review)
    # review=b.correct()
    # print(review)
    # review = review.split()
    # ps = PorterStemmer()
    # review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    # review = ' '.join(review)
    corpus.append(review)

cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

MaxFeatures=20000;
print(X.shape)
X_train = sequence.pad_sequences(X_train, maxlen=MaxFeatures)
X_test = sequence.pad_sequences(X_test, maxlen=MaxFeatures)
print(X.shape)
classifier = Sequential()
# # Adding the input layer and the first hidden layer
classifier.add(Dense(units = 100, kernel_initializer = 'uniform', activation = 'relu', input_dim = MaxFeatures))
classifier.add(Dense(units = 100, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 100, kernel_initializer = 'uniform', activation = 'relu'))
classifier.add(Dense(units = 3, kernel_initializer = 'uniform', activation = 'softmax'))
from keras import optimizers
optimizer=optimizers.adam()
classifier.compile(optimizer = optimizer, loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
history=classifier.fit(X_train, y_train,validation_split=0.33, batch_size = 30, epochs =2)
classifier.save('Learnings/nnClassifier')
filename = 'Learnings/nn_vectorizer.pkl'
fileObject = open(filename,'wb')
pickle.dump(cv,fileObject)

fileObject.close()

import matplotlib.pyplot as plt
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
print(history)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

print('hello')



from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
y_pred=classifier.predict_classes(X_test,batch_size=10)
target_names = ['Neutral', 'Positive','Negative']
confusionMatrix = confusion_matrix(y_test, y_pred,labels=[0,1,2])
print(confusionMatrix)
print(classification_report(y_test, y_pred, target_names=target_names))
print("Accuracy :",accuracy_score(y_test,y_pred,normalize=True)
print(classifier.summary())