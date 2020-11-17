import os
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import Callback 

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        return text


class SavingCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        ckpt_path = os.path.join(os.path.join(os.path.dirname(__file__), 'checkpoints'))
        if epoch < 10:
            for fn in os.listdir(ckpt_path):
                if 'ckpt' in fn:
                    os.remove(os.path.join(ckpt_path, fn))
        else:
            #extract all saved epochs from filenames
            saved_epochs = [int(re.sub(r"[ckpt_, .index]","", fn)) for fn\
                             in os.listdir(ckpt_path) if ".index" in fn]
            saved_epochs.sort()
            #leave just 2 checkpoints
            if len(saved_epochs) > 2:
                epochs_to_delete = saved_epochs[:-2]
                for epoch in epochs_to_delete:
                    fn = f"ckpt_{epoch}.data-00000-of-00001"
                    os.remove(os.path.join(ckpt_path, fn))
                    fn = f"ckpt_{epoch}.index"
                    os.remove(os.path.join(ckpt_path, fn))


def save_tokenizer(tokenizer, model_type="many_to_one"):
    save_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 
                f'tokenizer_{model_type}.pickle')
    if os.path.exists(save_path):
        os.remove(save_path)

    with open(save_path, 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_tokenizer(model_type="many_to_one"):
    save_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 
                f'tokenizer_{model_type}.pickle')
    with open(save_path, 'rb') as f:
        tokenizer = pickle.load(f)
        return tokenizer
            