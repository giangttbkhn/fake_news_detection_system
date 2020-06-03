import datetime
import requests
import nltk
from pycorenlp import StanfordCoreNLP
from pyspark import SparkContext, SparkConf
conf = SparkConf().setAppName("app")
sc = SparkContext(conf=conf)

def telegram_bot_sendtext(service_name, time, type, bot_message):
    bot_token = '1297258570:AAGTzLSNjMrE9gLhpJuQ2EOyL45Bb5yGwZc'
    bot_chatID = '-467351323'
    mess = type + '\t' + service_name + '\n' + time + '\n' + bot_message
    mess = mess.replace('_', '-')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + mess
    response = requests.get(send_text)
    return response.json()

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

def extracter(sent):
    output= nlp.annotate(sent, properties={'annotators': 'tokenize, ssplit, pos, depparse, parse, openie','outputFormat': 'json'})
    triple = []
    try:
        for item in output['sentences'][0]['openie']:
            tmp = item['subject'].replace(" ", "_") + "\t" + format_relation(item['relation']) + "\t" + item["object"].replace(" ", "_")
            triple.append(tmp)
        return triple
    except Exception as e:
        return repr(e)
        

def filter_trump(triple):
    return triple.lower().__contains__('trump')

site = 'dailymail'
now = datetime.datetime.now()
distTime = now - datetime.timedelta(1)
folder_name = distTime.__format__("%Y-%m-%d")
#folder_name = "2020-05-27"
folder_input = "/user/hduser/processed_data/"+site+"/"+folder_name+"/*"
foler_save = "hdfs:///user/hduser/triples/"+site+"/"+folder_name+".txt"
time_now = now.__format__('%Y-%m-%d %H:%M:%S')
try:
    telegram_bot_sendtext("extraction.py", time_now, "INFO", "Start extracting triples from " + site + ", date: " + folder_name)
    data = sc.textFile(folder_input)
    data2 = data.map(lambda x: nltk.sent_tokenize(x)[0])
    nlp = StanfordCoreNLP('http://localhost:9000')
    out = data2.flatMap(lambda x: extracter(x))
    res = out.filter(lambda x: filter_trump(x))
    res.saveAsTextFile(foler_save)

    time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    telegram_bot_sendtext("extraction.py", time_now, "INFO", "Successfully extract triples from " + site + ", date: " + folder_name)
except Exception as e:
    mess = "ERROR when extract tripple news from " +site+", date: " + folder_name + "\n" + repr(e)
    time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    telegram_bot_sendtext("extraction.py", time_now, "ERROR", mess)
