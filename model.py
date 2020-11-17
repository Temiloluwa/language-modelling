import tensorflow as tf
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from  tensorflow.keras.layers import Embedding, LSTM, Dense
import numpy as np

def many_to_one_model(vocab_size,
                      sequence_len,
                      embedding_dims,
                      lstm_dims,
                      dense_dims):

    model = tf.keras.Sequential([
        Embedding(vocab_size, embedding_dims, input_length=sequence_len),
        LSTM(lstm_dims, return_sequences=True),
        LSTM(lstm_dims),
        Dense(dense_dims, activation='relu'),
        Dense(dense_dims, activation='softmax')
    ])

    return model


def generate_words(start_string, num_words, temperature, model, tokenizer, sequence_len, padding_value=0):
    model.reset_states()
    punctuation_to_keep = r"[!:.;,?\t\n]"
    start_string = re.sub(punctuation_to_keep, lambda x: " " + x.group(0) + " ", start_string)
    start_string.split(" ")
    
    start_sequence = tokenizer.texts_to_sequences([start_string])[0]
    start_sequence = np.expand_dims(np.array(start_sequence),0)
    sequence = pad_sequences(start_sequence, maxlen=sequence_len, value=padding_value)

    generated_text = []
    for i in range(num_words):
        prediction = model.predict(sequence)
        prediction /= temperature
        predicted_id = int(tf.random.categorical(prediction,1))
        generated_text.append(predicted_id)
        sequence = np.concatenate((sequence[:, 1:], np.array([[predicted_id]])), axis=1)
        
    generated_text = [tokenizer.index_word[i] for i in generated_text if i != 0]
    generated_text = " ".join(generated_text)
    return generated_text



