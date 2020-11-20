"""Prediction of User based on tweet embeddings."""

import numpy as np
import spacy
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
from flask import request
import en_core_web_lg

# nlp = en_core_web_lg.load()
nlp = spacy.load("en_core_web_lg")
dataframe1 = 'https://raw.githubusercontent.com/jrivest2/kickstarter_success_bw/main/live.csv'
data = pd.read_csv(dataframe1)

vectorized = [nlp(text).vector for text in data['blurb']]

pca = PCA(n_components=2)

pca.fit(vectorized)

word_vecs_2d = pca.transform(vectorized)


rfr = RandomForestRegressor(n_jobs=10)

X = word_vecs_2d
y = data['percentage.funded']
RFR_Fit = rfr.fit(X,y)


filename = 'kickstarter_model.pkl'
pickle.dump(RFR_Fit, open(filename, 'wb'))
final_model = pickle.load(open(filename, 'rb'))

y_pred = final_model.predict(X)
accuracy = final_model.score(X,y)
def predict_success(projectName,input):
    
    dummy = nlp(input).vector
    dummy2 = pca.transform([dummy])
    output = final_model.predict(dummy2)[0]
    
    message = "There is a {:.2f}% chance that the {} project will get {}% of their funding goal.".format(
                accuracy*100, projectName, output)
    return message
