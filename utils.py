import os

def read_text_file(file_path):
    """Read text file and return arrays

    Args:
        path (file_path): path to file

    Returns:
        lines_list (list): list strings per line
    """ 
    with open(file_path, "r", encoding="utf-8") as f:
        temp = f.readlines()
        temp = [i.strip("\n") for i in temp]
        lines_list = [i for i in temp if i != ''] 
        return lines_list


def int_to_word_mappings():
    pass