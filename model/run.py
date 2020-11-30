import tensorflow as tf
import os
import pickle
from tensorflow.keras.losses import sparse_categorical_crossentropy
from data import many_to_one_data
from model import many_to_one_model, generate_words
from utils import SavingCallback, save_tokenizer, load_tokenizer, load_config, \
                cache_checkpoints, load_model
from app import app

config = load_config()
MODE = config.mode
hyp  = config.hyperparameters 
SEQ_LEN = hyp.sequence_length
BATCH_SIZE = hyp.batch_size
SHUFFLE_BUFFER_SIZE = hyp.shuffle_buffer_size
EMBED_DIMS = hyp.embedding_dims
LSTM_DIMS = hyp.lstm_dims
EPOCHS = hyp.epochs
LEARNING_RATE = hyp.learning_rate
VOCAB_SIZE = hyp.vocab_size

DATA_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'shakespeare.txt')
ckpt_dir = os.path.join(os.path.dirname(__file__), 'checkpoints')
ckpt_prefix = os.path.join(ckpt_dir, 'ckpt_{epoch}')
ckpt_callback = tf.keras.callbacks.ModelCheckpoint(
                    monitor='loss',
                    filepath=ckpt_prefix,
                    save_weights_only=True,
                    save_best_only=True,
                    save_freq='epoch')

def loss(labels, logits):
    return sparse_categorical_crossentropy(labels, logits, from_logits=True)

if __name__ == "__main__":
    if MODE == "train":
        dataset, tokenizer = many_to_one_data(DATA_PATH, SEQ_LEN, VOCAB_SIZE)  
        dataset = tf.data.Dataset.from_tensor_slices(dataset).shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
        save_tokenizer(tokenizer)
        dataset = dataset.map(lambda x: (x[:,:-1], x[:,-1])) # last word is the target
        model = many_to_one_model(VOCAB_SIZE, SEQ_LEN, EMBED_DIMS, LSTM_DIMS, dense_dims=VOCAB_SIZE)
        optimizer = tf.keras.optimizers.Adam(lr=LEARNING_RATE)
        model.compile(optimizer=optimizer, loss=loss)
        history = model.fit(dataset, epochs=EPOCHS, callbacks=[ckpt_callback, SavingCallback()])
        cache_checkpoints(config)
    elif MODE == "inference":
        start_string = input("Enter the Start String?")
        model = load_model(start_string, os.path.join(ckpt_dir, f'exp_{config.experiment}'))
        generated_words = generate_words(start_string, 
                                        num_words=500, 
                                        temperature=0.9, 
                                        model=model, 
                                        tokenizer=tokenizer, 
                                        sequence_len=SEQ_LEN, 
                                        padding_value=0)
        print(generated_words)
    else:
        app.run()


    



