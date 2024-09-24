import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import re
from keras.preprocessing.text import tokenizer_from_json
import json

# Text preprocessing
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def load_tokenizer():
    # Loading the Tokenizer
    with open('models/tokenizer.json', 'r', encoding='utf-8') as f:
        tokenizer_data = json.load(f)
    # Convert a dictionary to JSON string format
    tokenizer_json_str = json.dumps(tokenizer_data)
    tokenizer = tokenizer_from_json(tokenizer_json_str)
    return tokenizer


def load_pretrained_model():
    model = load_model('models/cnn_w2v.h5')
    return model

# Using the model to predict sentiment
def predict_emotion(text, model, tokenizer):
    cleaned_text = clean_text(text)
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded_sequence = pad_sequences(sequence, maxlen=500)
    prediction = model.predict(padded_sequence)
    class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']
    return class_names[np.argmax(prediction)]
