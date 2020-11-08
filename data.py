import os
import nltk
from utils import read_text_file


data_path = os.path.join(os.path.dirname(__file__), 'datasets', 'shakespeare.txt')
list_of_lines = read_text_file(data_path)
print(len(list_of_lines))
