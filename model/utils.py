import os
import pickle
import re
import json
import shutil
from easydict import EasyDict as edict
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import Callback 

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        return text


class SavingCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        ckpt_path = os.path.join(os.path.join(os.path.dirname(__file__), 'checkpoints'))
        if epoch > 3:
            #extract all saved epochs from filenames
            saved_epochs = [int(re.sub(r"[ckpt_, .index]","", fn)) for fn\
                             in os.listdir(ckpt_path) if ".index" in fn]
            saved_epochs.sort()
            #leave just 2 checkpoints
            if len(saved_epochs) > 2:
                epochs_to_delete = saved_epochs[:-2]
                for epoch in epochs_to_delete:
                    for fn in os.listdir(ckpt_path):
                        if not os.path.isdir(fn):
                            if f"ckpt_{epoch}" in fn:
                                os.remove(os.path.join(ckpt_path, fn))


def save_tokenizer(tokenizer, model_type="many_to_one"):
    save_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 
                f'tokenizer_{model_type}.pickle')
    if os.path.exists(save_path):
        os.remove(save_path)

    with open(save_path, 'wb') as f:
        pickle.dump(tokenizer, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_tokenizer(config, model_type="many_to_one"):
    save_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 
                f'exp_{config.experiment}', f'tokenizer_{model_type}.pickle')
    with open(save_path, 'rb') as f:
        tokenizer = pickle.load(f)
        return tokenizer
            

def load_config(config_path: str="config.json"):
    """Loads config file"""
    config_path = os.path.join(project_root, config_path)
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    return edict(config)


def cache_checkpoints(config):
    ckpt_path = os.path.join(project_root, 'checkpoints')
    ckpt_final_path = os.path.join(ckpt_path, f'exp_{config.experiment}')
    os.makedirs(ckpt_final_path, exist_ok=True)
    config_path = os.path.join(ckpt_final_path, "config_f'exp_{config.experiment}'.json")
    for fn in os.listdir(ckpt_path):
        src = os.path.join(ckpt_path, fn)
        if not os.path.isdir(src):
            dest = os.path.join(ckpt_final_path, fn)
            if shutil.copy2(src, dest):
                os.remove(src)
    with open(config_path, "w",  encoding="utf-8") as f:
        json.dump(config, f, indent=4)


project_root = os.path.dirname(os.path.realpath(__file__))
