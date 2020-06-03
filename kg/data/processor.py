import traceback

from model.model import Entity, Relation, Triple
import os
import re
from pycorenlp import StanfordCoreNLP

STANDFORD_CORE_URI = 'http://localhost:9000'
class DataProcessor:
    def __init__(self, files=None):
        self.sources = files
        self.triples = []
        self.news = ""
        self.nlp = StanfordCoreNLP('http://localhost:9000')

    def add_source(self, files):
        self.sources = files

    def generate_triples(self):
        for source in self.sources:
            if os.path.exists(source):
                with open(source) as file:
                    lines = file.readlines()
                    for line in lines:
                        [h, r, t] = line.split()
                        triple = self._create_triple(h, t, r)
                        self.triples.append(triple)
        return self.triples

    def analyse_input(self):
        # nlp = StanfordCoreNLP('http://localhost:9000')
        # text = "'Tom be 42 years old, Tom be a teacher'"
        output = self.nlp.annotate(self.news, properties={
            'annotators': 'tokenize, ssplit, pos, depparse, parse, openie',
            'outputFormat': 'json'
        })

        self.triples = []
        try:
            for item in output['sentences'][0]['openie']:
                tmp = item['subject'].replace(" ", "_") + "\t" \
                      + self._format_relation(item['relation']) + "\t" \
                      + item["object"].replace(" ", "_")
                [h, r, t] = tmp.split()
                triple = self._create_triple(h,t,r)
                self.triples.append(triple)
                # triple.append(tmp)
        except:
            # traceback.print_exc()
            pass
        # print(triple)

    # def solve_sentence(self, sentence):
    #     sentence = "Trump_campaign_spokeswoman	willPutFirst	America"
    #     nhead = "Trump_campaign_spokeswoman"
    #     nrelation = "willPutAt"
    #     ntail = "America"
    #     return self._create_triple(nhead, ntail, nrelation)

    def _create_triple(self, nhead="", ntail="", nrelation=""):
        head = Entity(nhead.replace("\'", "`"))
        relation = Relation(nrelation.replace("\'", "`"), re.sub('[^a-zA-Z \n_]', '', nrelation))
        tail = Entity(ntail.replace("\'", "`"))
        return Triple(head, relation, tail)

    def _format_relation(self,str):
        arr = [pos for pos, char in enumerate(str) if char == " "]

        result = ""
        for index, item in enumerate(str):
            if (index - 1) in arr:
                result += item.upper()
            else:
                result += item

        result = result.replace(" ", "")

        return result


class InputProcessor:
    def __init__(self, str=None):
        self.sentence = str
        self.triples = []

    def analyse_input(self):
        nlp = StanfordCoreNLP('http://localhost:9000')
        # text = "'Tom be 42 years old, Tom be a teacher'"
        output = nlp.annotate(self.sentence, properties={
            'annotators': 'tokenize, ssplit, pos, depparse, parse, openie',
            'outputFormat': 'json'
        })

        triple = []
        try:
            for item in output['sentences'][0]['openie']:
                tmp = item['subject'].replace(" ", "_") + "\t" \
                      + self._format_relation(item['relation']) + "\t" \
                      + item["object"].replace(" ", "_")

                [h,r,t] = tmp.split()
                triple.append(tmp)
            self.triples = triple
        except:
            pass

    def _format_relation(str):
        arr = [pos for pos, char in enumerate(str) if char == " "]

        result = ""
        for index, item in enumerate(str):
            if (index - 1) in arr:
                result += item.upper()
            else:
                result += item

        result = result.replace(" ", "")

        return result


if __name__ == "__main__":
    my_str = "'_hey.th~!ere"
    my_new_string = re.sub('[^a-zA-Z0-9 \n_]', '', my_str)
    print(my_new_string)
