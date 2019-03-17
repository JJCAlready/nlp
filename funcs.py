import tensorflow as tf
import re

# Open the files and load it
def open_ds(f_lines, f_conversations):
    lines = open(f_lines, encoding='utf-8', errors='ignore').read().split('\n')
    conversations = open(f_conversations, encoding='utf-8', errors='ignore').read().split('\n')
    return lines, conversations


# Create a list with lines
def dict_line_id(lines, id2line):
    for line in lines:
        _line = line.split(' +++$+++ ')
        if len(_line) == 5:
            id2line[_line[0]] = _line[4]
    return id2line

# Create a list with conversations
def list_conversations(conversations, conversations_ids):
    for conversation in conversations[:-1]:
        _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
        conversations_ids.append(_conversation.split(','))
    return conversations_ids


# Separate questions and answers in two lists
def div_quest_ans(conversations_ids, questions, answers, id2line):
    for conversation in conversations_ids:
        for i in range(len(conversation) - 1):
            questions.append(id2line[conversation[i]])
            answers.append(id2line[conversation[i + 1]])
    return questions, answers


# Performs a standarization of the text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text


# Create a dictionary  with pairs of words and numbers
def create_dict(word2count, words2int, threshold):
    word_number = 0
    for word, count in word2count.items():
        if count >= threshold:
            words2int[word] = word_number
            word_number += 1
    return words2int


def qa2int(clean_txt, words2int, text_into_int):
    for question in clean_txt:
        ints = []
        for word in question.split():
            if word not in words2int:
                ints.append(words2int['<OUT>'])
            else:
                ints.append(words2int[word])
        text_into_int.append(ints)
    return text_into_int


def dict_number_occur(clean_txt, word2count):
    for txt in clean_txt:
        for word in txt.split():
            if word not in word2count:
                word2count[word] = 1
            else:
                word2count[word] += 1
    return word2count
