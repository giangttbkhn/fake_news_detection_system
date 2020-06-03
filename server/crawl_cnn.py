from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
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
    results = luanvan_results.find_elements_by_tag_name("div")

    return len(results)


def save_to_hdfs(site, folder_name):
    try:
        now = datetime.datetime.now()
        time_now = now.__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_cnn.py", time_now, "INFO",
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
        telegram_bot_sendtext("crawl_cnn.py", time_now, "INFO",
                              "Successfully save to HDFS from: " + site + ", date: " + folder_name)
    except Exception as e:
        mess = "ERROR when save to HDFS from " + site + ", date: " + folder_name + "\n" + repr(e)
        time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_cnn.py", time_now, "ERROR", mess)

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
        telegram_bot_sendtext("crawl_cnn.py", time_now, "INFO", "Start pre_processing news from: " + data_name)
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
        telegram_bot_sendtext("crawl_cnn.py", time_now, "INFO", "Successfully pre_processing news from: " + data_name)
        return
    except Exception as e:
        mess = "ERROR when pre_processing news from " + data_name + "\n" + repr(e)
        time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        telegram_bot_sendtext("crawl_cnn.py", time_now, "ERROR", mess)

site = 'cnn'
now = datetime.datetime.now()
distTime = now - datetime.timedelta(1)
# folder_name = "2020-05-25"
folder_name = distTime.__format__("%Y-%m-%d")
time_now = now.__format__('%Y-%m-%d %H:%M:%S')
DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"
try:
    telegram_bot_sendtext("crawl_cnn.py", time_now, "INFO",
                          "Start crawling news from " + site + ", date: " + folder_name)

    pattern_url = "https://edition.cnn.com/"
    key_search = "donald trump"
    path_save = DIR_PATH + site
    key_search_pattern = key_search.replace(" ", "%20")

    pattern_next = "https://edition.cnn.com/search?q=" + key_search_pattern + \
                   "&size=10&page=@page@&from=@index@&category=us,politics,world,opinion,health"

    options = webdriver.ChromeOptions()
    #chrome_options = Options()

    #chrome_options.add_argument('--no-sandbox')

    #chrome_options.add_argument('--headless')

    #chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(DIR_PATH + "chromedriver/chromedriver", chrome_options=options)

    driver.get(pattern_url)

    search = driver.find_element_by_xpath(
        '//*[@id="footer-wrap"]/footer/div/div/form/input')

    search.send_keys(key_search)
    search.send_keys(Keys.ENTER)

    news_type = driver.find_element_by_xpath('//*[@id="left_news"]')
    news_type.click()

    # tmp1 = pattern_next
    # tmp1 = tmp1.replace("@page@", str(13))
    # tmp1 = tmp1.replace("@index@", str((13-1)*10))
    # driver.get(tmp1)
    # time.sleep(3)

    with open(path_save + "/" + "definition.txt", 'r') as f:
        down_files = f.read()

    down_files = down_files.split("\n")

    path_save_ = path_save + "/" + folder_name

    if os.path.isdir(path_save_) == False:
        os.makedirs(path_save_)

    page = 2
    count_overlap = 0
    count_time = 0
    total_time = 0
    while (1):

        tmp_time = datetime.datetime.now()
        i = 1
        current_url = driver.current_url

        if count_overlap >= 5:
            break

        while i <= 10:
            try:
                article = driver.find_element_by_xpath('//*[@class="cnn-search__results-list"]/div[' +
                                                       str(i) + ']/div[2]/h3/a')
                is_video = article.get_attribute('href')

                if 'video' in is_video or 'world' in is_video:
                    i += 1
                    pass
                elif '2020' in is_video:
                    i += 1
                    try:
                        article.click()

                        title = driver.find_element_by_xpath('//*[@class="pg-headline"]').text

                        file_name = ''.join(e for e in title if e.isalnum())

                        if any(file_name in s for s in down_files):
                            count_overlap += 1
                            continue

                        content = driver.find_element_by_xpath('//*[@class="pg-rail-tall__body"]/section/div').text

                        with open(path_save_ + "/" + file_name + ".txt", 'w') as f:
                            f.write(title)
                            f.write("\n\n")
                            f.write(content)

                        down_files.append(file_name)
                        with open(path_save + "/" + "definition.txt", 'a') as f:
                            f.write("\n")
                            f.write(file_name)

                        tmp = datetime.datetime.now() - tmp_time
                        count_time += 1
                        total_time += tmp.total_seconds()

                        driver.execute_script("window.history.go(-1)")
                        time.sleep(3)
                    except:
                        driver.get(current_url)
                else:
                    i += 1

            except:
                i += 1
                driver.get(current_url)

        tmp = pattern_next
        tmp = tmp.replace("@page@", str(page))
        tmp = tmp.replace("@index@", str((page - 1) * 10))
        driver.get(tmp)
        page += 1
        time.sleep(3)
    driver.quit()
    print(total_time)
    print(count_time)
    print(total_time / count_time)
    mess = "Total file craw: " + str(count_time) + "\nTotal time: " + str(total_time) + "\nAVG: " + str(
        total_time / count_time)
    time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    telegram_bot_sendtext("crawl_cnn.py", time_now, "INFO", mess)
except Exception as e:
    mess = "ERROR when crawl news from " + site + ", date: " + folder_name + "\n" + repr(e)
    time_now = datetime.datetime.now().__format__('%Y-%m-%d %H:%M:%S')
    telegram_bot_sendtext("crawl_cnn.py", time_now, "ERROR", mess)

pre_processing(site)

save_to_hdfs(site, folder_name)
