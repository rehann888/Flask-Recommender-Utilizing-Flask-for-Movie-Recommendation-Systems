import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_distances
import nltk
nltk.download('punkt')

class content_base_filtering:
    def __init__(self, data, content_col):
        self.df = pd.read_csv(data)
        self.content_col = content_col
        self.encoder = None
        self.bank = None

    def fit(self):
        self.encoder = CountVectorizer(stop_words="english", tokenizer=word_tokenize)
        self.bank = self.encoder.fit_transform(self.df[self.content_col])

    def recommend(self, title, top=10):
        content = self.df[self.df['title'] == title]
        numeric = self.encoder.transform(content[self.content_col])
        numeric = numeric.toarray()  
        dist = cosine_distances(numeric, self.bank)
        rec = dist.argsort()[0, 1:(top+1)]
        recommended_df = self.df.iloc[rec].reset_index(drop=True)
        recommended_df['No'] = np.arange(1, len(recommended_df) + 1)
        return recommended_df.iloc[:, :2]
