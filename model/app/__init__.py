from flask import Flask
from flask_restful import Api
from flask_cors import CORS
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/generatewords": {"origins": "*"}})
from app import views