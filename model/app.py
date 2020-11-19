import os
import tensorflow as tf
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from utils import load_tokenizer, load_config
from model import many_to_one_model, generate_words

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/generatewords": {"origins": "*"}})

ckpt_dir = os.path.join(os.path.dirname(__file__), 'checkpoints', 'exp_1')
config = load_config(os.path.join(ckpt_dir, 'config.json'))
hyp  = config.hyperparameters
SEQ_LEN = hyp.sequence_length
BATCH_SIZE = hyp.batch_size
SHUFFLE_BUFFER_SIZE = hyp.shuffle_buffer_size
EMBED_DIMS = hyp.embedding_dims
LSTM_DIMS = hyp.lstm_dims
VOCAB_SIZE = hyp.vocab_size
tokenizer = load_tokenizer(config)
model = many_to_one_model(VOCAB_SIZE, SEQ_LEN, EMBED_DIMS, LSTM_DIMS, dense_dims=VOCAB_SIZE)
model.load_weights(tf.train.latest_checkpoint(os.path.join(ckpt_dir)))
model.build(tf.constant(1, None, SEQ_LEN))


parser = reqparse.RequestParser()
parser.add_argument('start-string', type=str)

class GenerateWords(Resource):
    def post(self):
        args = parser.parse_args()
        response_text = self.generate_words(args.get("start-string"))
        response = {"status":200, "msg": response_text}
        return jsonify(response)


    def generate_words(self, start_string):
        generated_words = generate_words(start_string, 
                                        num_words=500, 
                                        temperature=0.9, 
                                        model=model, 
                                        tokenizer=tokenizer, 
                                        sequence_len=SEQ_LEN, 
                                        padding_value=0)
        return generated_words


api.add_resource(GenerateWords, '/generatewords')
if __name__ == "__main__":
    app.run(host="0.0.0.0")
   