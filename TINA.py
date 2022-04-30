import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import pandas as pd

with open("intents.json") as file:
    data = json.load(file)

with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.load("model.tflearn")    

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def chat(input):
    while True:
        results = model.predict([bag_of_words(input, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            reply = random.choice(responses)
            if reply == "recommend":
                reply = Recommend()
                return reply
            elif reply == "best selling":
                reply = BestSelling()
                return reply
            else:
                return reply
        else:
            return "I didn't get that, try again."

def Recommend():
    df = pd.read_excel('Cake_List.xlsx')
    final_data = df.sort_values('Ratings')
    new_data = final_data.tail()
    best_names = new_data['Name'].to_list()
    str_ = ""
    count = 0
    for n in best_names:
        if count == len(best_names)-1:
            str_ = str_ + n + "."
        else:
            str_ = str_ + n + ", "
            count +=1
    return "Our bestselling cakes are as follows: " + str_

def BestSelling():
    df = pd.read_excel('Cake_List.xlsx')
    all_names = df['Name'].to_list()
    all_ratings = df['Ratings'].to_list()
    return "According to our customers " + str(all_names[all_ratings.index(max(all_ratings))]) + " is our best selling cake "