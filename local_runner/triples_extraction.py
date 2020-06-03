import os
import nltk
from pycorenlp import StanfordCoreNLP

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"

#data folder
path = DIR_PATH + "test1"

def format_relation(str):
    arr = [pos for pos, char in enumerate(str) if char == " "]

    result = ""
    for index, item in enumerate(str):
        if (index - 1) in arr:
            result += item.upper()
        else:
            result += item

    result = result.replace(" ", "")

    return result

text = ""
for item in os.listdir(path):
    with open(path + "/" + item, 'r') as f:
        text += "\n" + f.read()

sents_text = nltk.sent_tokenize(text[1:])

nlp = StanfordCoreNLP('http://localhost:9000')

triples = []
i = 0
for sent in sents_text:
    print (i)
    output = nlp.annotate(sent, properties={
        'annotators': 'tokenize, ssplit, pos, depparse, parse, openie',
        'outputFormat': 'json'
    })

    try:
        triple = []
        for item in output['sentences'][0]['openie']:
            tmp = item['subject'].replace(" ", "_") + "\t" \
                  + format_relation(item['relation']) + "\t" \
                  + item["object"].replace(" ", "_")

            triple.append(tmp)

        triples += triple
    except:
        print (sent)

    i += 1

with open("test1.txt", "w") as f:
    f.write("\n".join(triples))

#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000