from selenium import webdriver
import time
import os
import spacy
import neuralcoref
import nltk
import datetime
import re
import requests


def telegram_bot_sendtext(service_name, time, type, bot_message):
    bot_token = '1297258570:AAGTzLSNjMrE9gLhpJuQ2EOyL45Bb5yGwZc'
    bot_chatID = '-467351323'
    mess = type + '\t' + service_name + '\n' + time + '\n' + bot_message
    mess = mess.replace('_', '-')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + mess
    response = requests.get(send_text)
    return response.json()


def count_luanvan(luanvan_results):
    results = luanvan_results.find_elements_by_tag_name("article")
    return len(results)


def save_to_hdfs(site, folder_name):
    try:
        now = datetime.datetime.now()
        time_now = now.__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_foxnews.py", time_now, "INFO",
                              "Start save to HDFS from: " + site + ", date: " + folder_name)
        from subprocess import PIPE, Popen
        processed_path = DIR_PATH + "processed_data/" + site + "/" + folder_name + "/"
        hdfs_path = "/user/hduser/processed_data/" + site
        # put = Popen(["hadoop", "fs", "-mkdir", file_name, "/user/hduser/giangtt/abc/"], stdin=PIPE, bufsize=-1)
        # put.communicate()
        # put csv into hdfs
        put = Popen(["/home/hduser/hadoop-2.7.7/bin/hadoop", "fs", "-copyFromLocal", processed_path, hdfs_path], stdin=PIPE, bufsize=-1)
        put.communicate()

        now = datetime.datetime.now()
        time_now = now.__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_foxnews.py", time_now, "INFO",
                              "Successfully save to HDFS from: " + site + ", date: " + folder_name)
    except Exception as e:
        mess = "ERROR when save to HDFS from " + site + ", date: " + folder_name + "\n" + repr(e)
        time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_foxnews.py", time_now, "ERROR", mess)

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
        # text_ = nltk.word_tokenize(item)
        # tag = nltk.pos_tag(text_)

        # tmp = item
        # for item2 in tag:
        #     # print(item[1])
        #     if "VB" in item2[1]:
        #         verb_inf = nltk.stem.WordNetLemmatizer().lemmatize(item2[0], 'v')

        #         tmp = tmp.replace(item2[0], verb_inf)

        sents_result.append(item)

    return sents_result


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


def pre_processing(data_name):
    try:
        now = datetime.datetime.now()
        time_now = now.__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_foxnews.py", time_now, "INFO", "Start pre_processing news from: " + data_name)
        DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"
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
                    print(file_name)
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
        now = datetime.datetime.now()
        time_now = now.__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_foxnews.py", time_now, "INFO", "Successfully pre_processing news from: " + data_name)
        return
    except Exception as e:
        mess = "ERROR when pre_processing news from " + data_name + "\n" + repr(e)
        time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_foxnews.py", time_now, "ERROR", mess)

site = 'news_fox'
now = datetime.datetime.now()
distTime = now - datetime.timedelta(1)
# folder_name = "2020-05-25"
folder_name = distTime.__format__("%Y-%m-%d")
time_now = now.__format__('%Y-%m-%d %H:%M:%S')
DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"
try:
    telegram_bot_sendtext("crawl_foxnews.py", time_now, "INFO",
                          "Start crawling news from " + site + ", date: " + folder_name)

    pattern_url = "https://www.foxnews.com/category/person/donald-trump"
    path_save = DIR_PATH + "news_fox"

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(DIR_PATH + "chromedriver/chromedriver", chrome_options=options)

    driver.get(pattern_url)

    contain = driver.find_element_by_xpath(
        '//*[@class="row"]/main/section/div')

    number = count_luanvan(contain)

    with open(path_save + "/" + "definition.txt", 'r') as f:
        down_files = f.read()

    down_files = down_files.split("\n")

    path_save_ = path_save + "/" + folder_name

    if os.path.isdir(path_save_) == False:
        os.makedirs(path_save_)

    i = 1
    count_overlap = 0

    count_time = 0
    total_time = 0
    while (1):

        tmp_time = datetime.datetime.now()
        if count_overlap >= 5:
            break

        try:
            link_article = driver.find_element_by_xpath(
                '//*[@class="row"]/main/section/div/article[' + str(i) + ']/div[1]/a')
            is_video = link_article.get_attribute('href')

            if 'video' in is_video:
                pass
            else:
                link_article.click()

                title = driver.find_element_by_xpath(
                    '//*[@class="headline"]').text

                content = driver.find_element_by_xpath(
                    '//*[@class="article-body"]').text

                file_name = ''.join(e for e in title if e.isalnum())

                if any("foxnews_" + file_name in s for s in down_files):
                    count_overlap += 1
                else:
                    with open(path_save_ + "/foxnews_" + file_name, 'w') as f:
                        f.write(title)
                        f.write("\n")
                        f.write(content)

                    down_files.append("foxnews_" + file_name)
                    with open(path_save + "/" + "definition.txt", 'a') as f:
                        f.write("\n")
                        f.write("foxnews_" + file_name)

                    count_time += 1
                    tmp = datetime.datetime.now() - tmp_time
                    total_time += tmp.total_seconds()

                driver.execute_script("window.history.go(-1)")
                time.sleep(3)
        except:
            pass

        count_ = driver.find_element_by_xpath(
            '//*[@class="row"]/main/section/div')
        count = count_luanvan(count_)

        if i >= count:
            while i >= count:
                load_more = driver.find_element_by_xpath(
                    '//*[@class="row"]/main/section/footer/div/a')
                load_more.click()

                time.sleep(2)
                count_ = driver.find_element_by_xpath(
                    '//*[@class="row"]/main/section/div')
                count = count_luanvan(count_)

        i += 1

    driver.quit()
    print(total_time)
    print(count_time)
    print(total_time / count_time)
    mess = "Total file craw: " + str(count_time) + "\nTotal time: " + str(total_time) + "\nAVG: " + str(
        total_time / count_time)
    time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    telegram_bot_sendtext("crawl_foxnews.py", time_now, "INFO", mess)
except Exception as e:
    mess = "ERROR when crawl news from " + site + ", date: " + folder_name + "\n" + repr(e)
    time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    telegram_bot_sendtext("crawl_foxnews.py", time_now, "ERROR", mess)
pre_processing(site)

save_to_hdfs(site, folder_name)
