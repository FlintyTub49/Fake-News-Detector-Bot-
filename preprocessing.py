# from tensorflow.keras.preprocessing import sequence
# import pickle as pk

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import numpy as np
import string
from bs4 import BeautifulSoup
import re
import os


# ---------------------------------
# Installing All The Prerequisites
# ---------------------------------
stop = set(stopwords.words('english'))
punctuation = list(string.punctuation)
stop.update(punctuation)
lem = WordNetLemmatizer()

# codePath = os.path.dirname(os.path.abspath('preprocessing.py'))
# tokens = os.path.join(codePath, 'Models/listone.pk')
# tokenizer = pk.load(open(tokens, 'rb'))


# -----------------------------------
# Defining All The Cleaning Functions
# -----------------------------------
# Removing HTML
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


# Removing the square brackets
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)


# Removing URL's
def remove_URL(text):
    return re.sub(r'http\S+', '', text)


# Removing the stopwords from text
def remove_stopwords(text):
    final_text = []
    for i in text.split():
        if i.strip().lower() not in stop:
            final_text.append(lem.lemmatize(i.strip()))
    return " ".join(final_text)


# Removing Emojis From Text
def remove_emojis(text):
    emojis = re.compile(pattern="["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)
    return emojis.sub(r'', text)


# Calling Function Which Class All Other Functions
def denoise_text(text):
    # Remove Emojis
    text = remove_emojis(text)

    # Remove HTML
    text = strip_html(text)

    # Remove Square Brackets
    text = remove_between_square_brackets(text)

    # Remove URLs
    text = remove_URL(text)

    # Remove Stopwords
    text = remove_stopwords(text)

    return text


# ---------------------------------
# Main Preprocess Function
# ---------------------------------
def preprocess_text(text):

    # Clean The User Given Text
    text = denoise_text(text)

    # Specifying Max Length Of The Data
    # maxlen = 90
    # tokenized_user = tokenizer.texts_to_sequences([text])
    # user = sequence.pad_sequences(tokenized_user, maxlen=maxlen)

    # Returning User A Cleaned Text
    return text
