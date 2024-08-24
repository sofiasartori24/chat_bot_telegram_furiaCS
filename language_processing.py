import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
import pandas as pd

class LanguageProcessing:
    def __init__(self) -> None:
        self.df = pd.read_csv('bot_training_data.csv')
        self.training_data = [(row['Sentence'].split(), row['Intent']) for _, row in self.df.iterrows()]
        self.training_set = [(self.extract_features(word_tokenize(" ".join(sentence))), intent) for sentence, intent in self.training_data]
        self.classifier = NaiveBayesClassifier.train(self.training_set)

    def extract_features(self, words):
        return {word: True for word in words}

    def detect_intent(self, user_input):
        features = self.extract_features(word_tokenize(user_input))
        return self.classifier.classify(features)

