import os
import spacy
import neuralcoref
import nltk
import datetime
import re

def pro_data(text):
    tmp = text.split("\n")

    result = []
    for item in tmp:
        if len(item) < 5:
            continue

        if "." in item[-3:]:
            result.append(item)
        else:
            result.append(item + ".")

    article = "\n".join(result)

    nlp = spacy.load('en')  # this is the line where it crashes
    neuralcoref.add_to_pipe(nlp)

    doc = nlp(article)

    article = doc._.coref_resolved

    sents = nltk.sent_tokenize(article)
    # print (sents)
    sents_result = []
    for item in sents:
        text_ = nltk.word_tokenize(item)
        tag = nltk.pos_tag(text_)

        tmp = item
        for item2 in tag:
            # print(item[1])
            if "VB" in item2[1]:
                verb_inf = nltk.stem.WordNetLemmatizer().lemmatize(item2[0], 'v')

                tmp = tmp.replace(item2[0], verb_inf)

        sents_result.append(tmp)

    return  sents_result

def pro_CNN(text):
    return text.replace("(CNN)", "")

def pro_dailymail(text):
    return text

def pro_foxnews(text):
    tmp = text.split("\n")

    results = []
    for item in tmp:
        if len(item.split(" ")) < 4:
            continue

        if "people are talking about this" in item:
            continue

        tmp1 = re.findall(u"\d+\:\d+\ \w+\ \-\ \w+\ \d+\,\ \d+", item)

        if len(tmp1) > 0:
            continue

        if "Twitter Ads info and privacy" in item:
            continue

        if "CLICK HERE" in item:
            continue

        results.append(item)

    return "\n".join(results)

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"

def runner(data_name):
# data_name = "news_fox" #cnn/dailymail/news_fox
    path_data = DIR_PATH + data_name
    path_save = DIR_PATH + "processed_data/" + data_name
    if os.path.isdir(path_save) == False:
        os.makedirs(path_save)

    for folder in os.listdir(path_data):
        if ".txt" in folder:
            continue

        if os.path.isdir(path_save + "/" + folder) == False:
            os.makedirs(path_save + "/" + folder)

            for file_name in os.listdir(path_data + "/" + folder):
                print (file_name)
                with open(path_data + "/" + folder + "/" + file_name, 'r') as f:
                    text = f.read()

                if data_name == "cnn":
                    text = pro_CNN(text)
                elif data_name == "news_fox":
                    text = pro_foxnews(text)
                else:
                    text = pro_dailymail(text)

                final_text = pro_data(text)

                # print (final_text)

                with open(path_save + "/" + folder + "/" + file_name, "w") as f:
                    f.write("\n".join(final_text))

        else:
            continue