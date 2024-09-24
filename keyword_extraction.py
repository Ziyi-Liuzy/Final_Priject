import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import networkx as nx
import numpy as np
import re

nltk.data.path.append('uuliuu/nltk_data') 

# Text preprocessing
def preprocess_text(text):
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Word segmentation
    words = word_tokenize(text) 
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word.isalpha()]
    return words

# Textrank keyword extraction function
def textrank_keyword_extraction(text, top_n=5, window_size=4):
    words = preprocess_text(text)
    word_set = list(set(words))
    # Create a mapping from words to indices
    word_index = {word: idx for idx, word in enumerate(word_set)}

    # Initialize the adjacency matrix of the co-occurrence graph
    graph = np.zeros((len(word_set), len(word_set)))

    # Create a co-occurrence map
    for i in range(len(words) - window_size + 1):
        window = words[i: i + window_size]
        for i in range(len(window)):
            for j in range(i + 1, len(window)):
                word1, word2 = window[i], window[j]
                # Update the edge weights of the co-occurrence graph
                if word1 in word_index and word2 in word_index:
                    graph[word_index[word1]][word_index[word2]] += 1
                    graph[word_index[word2]][word_index[word1]] += 1
    
    # Create a graph using NetworkX
    nx_graph = nx.from_numpy_array(graph)
    # Calculate the PageRank score for each word
    scores = nx.pagerank(nx_graph)
    # Sort by score
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    keywords = [word_set[idx] for idx, _ in sorted_words[:top_n]]
    
    return keywords

def extract_keywords(text, top_n=5):
    return textrank_keyword_extraction(text, top_n)
