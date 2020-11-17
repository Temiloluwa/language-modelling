import tensorflow as tf
import os
import pickle
from tensorflow.keras.losses import sparse_categorical_crossentropy
from data import many_to_one_data
from model import many_to_one_model, generate_words
from utils import SavingCallback, save_tokenizer, load_tokenizer


SEQ_LEN = 53
BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = int(1e5)
EMBED_DIMS = 60
LSTM_DIMS = 100
EPOCHS = 100
LEARNING_RATE = 1e-3
VOCAB_SIZE = 500
MODE = "GENERATE"

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

if MODE == "TRAIN":    
    dataset = tf.data.Dataset.from_tensor_slices(dataset).shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
    dataset, tokenizer = many_to_one_data(DATA_PATH, SEQ_LEN, VOCAB_SIZE)
    save_tokenizer(tokenizer)
    dataset = dataset.map(lambda x: (x[:,:-1], x[:,-1])) # last word is the target
    model = many_to_one_model(VOCAB_SIZE, SEQ_LEN, EMBED_DIMS, LSTM_DIMS, dense_dims=VOCAB_SIZE)
    optimizer = tf.keras.optimizers.Adam(lr=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss=loss)
    history = model.fit(dataset, epochs=EPOCHS, callbacks=[ckpt_callback, SavingCallback()])
else:
    tokenizer = load_tokenizer()
    start_string = "So what do we say about these things?"
    model = many_to_one_model(VOCAB_SIZE, SEQ_LEN, EMBED_DIMS, LSTM_DIMS, dense_dims=VOCAB_SIZE)
    model.load_weights(tf.train.latest_checkpoint(ckpt_dir))
    model.build(tf.constant(1, None, SEQ_LEN))
    generated_words = generate_words(start_string, 
                                     num_words=500, 
                                     temperature=0.9, 
                                     model=model, 
                                     tokenizer=tokenizer, 
                                     sequence_len=SEQ_LEN, 
                                     padding_value=0)
    print(generated_words)

    



