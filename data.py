import os
import re
import numpy as np
from utils import read_text_file
from tensorflow.keras.preprocessing.text import Tokenizer


def many_to_one_data(data_path, sequence_len, vocab_size):
    text = read_text_file(data_path)
    punctuation_to_keep = r"[!:.;,?\t\n]"
    text = re.sub(punctuation_to_keep, lambda x: " " + x.group(0) + " ", text)
    text = text.split(" ")
    list_of_texts = []
    idx = 0
    while idx + sequence_len + 1 <= len(text):
        list_of_texts.append(text[idx: idx + sequence_len + 1])
        idx += 1

    filters = re.sub(punctuation_to_keep, "", '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
    tokenizer = Tokenizer(num_words=vocab_size, filters=filters, char_level=False, oov_token="<oov>")
    tokenizer.fit_on_texts(list_of_texts)
    sequences = tokenizer.texts_to_sequences(list_of_texts)
    sequences = np.array(sequences)

    return sequences, tokenizer


