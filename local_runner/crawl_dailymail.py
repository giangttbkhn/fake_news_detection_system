from selenium import webdriver
import os
import time
import datetime

def count_luanvan(luanvan_results):
    results = luanvan_results.find_elements_by_tag_name("div")

    return len(results)

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"
pattern_url = "https://www.dailymail.co.uk/news/donald_trump/index.html"
path_save = DIR_PATH + "dailymail"

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(DIR_PATH + "chromedriver/chromedriver", chrome_options=options)

driver.get(pattern_url)

contain = driver.find_element_by_xpath(
                                '//*[@class="football-team-news"]')

number = int(count_luanvan(contain)/3)

i = 1

with open(path_save + "/" + "definition.txt", 'r') as f:
    down_files = f.read()

down_files = down_files.split("\n")

now = datetime.datetime.now()

folder_name = str(now).split(" ")[0].replace("-", "_")

path_save_ = path_save + "/" + folder_name

print (path_save_)

if os.path.isdir(path_save_) == False:
    os.makedirs(path_save_)

count_overlap = 0
count_time = 0
total_time = 0
while i < number:

    tmp_time = datetime.datetime.now()
    if count_overlap >= 10:
        break

    try:
        time.sleep(1)
        time_data = driver.find_element_by_xpath(
                                    '//*[@class="football-team-news"]/div[' + str(i) + ']/div/div/span').text
    except:
        time_data = driver.find_element_by_xpath(
            '//*[@class="football-team-news"]/div[' + str(i) + ']/div/span').text

    time_data = time_data.replace('/', '_').replace(':', '_')

    article = driver.find_element_by_xpath(
                                    '//*[@class="football-team-news"]/div[' + str(i) + ']/h2/a[1]')

    driver.execute_script("arguments[0].click();", article)

    title = driver.find_element_by_xpath(
                                    '//*[@id="js-article-text"]/h2[1]').text

    content = driver.find_element_by_xpath(
                                '//*[@id="js-article-text"]/div[2]').text

    text = title + "\n"
    for item in content.split('\n'):
        if len(item.split(' ')) < 5:
            continue

        if item[len(item)-3: ] == "...":
            continue

        text += item + "\n"

    i += 1

    if any("dailymail_" + time_data in s for s in down_files):
        count_overlap += 1
        driver.execute_script("window.history.go(-1)")
        time.sleep(3)
        continue

    with open(path_save_ +  '/dailymail_' + time_data, 'w') as f:
        f.write(text)

    down_files.append("dailymail_" + time_data)
    with open(path_save + "/" + "definition.txt", 'a') as f:
        f.write("\n")
        f.write("dailymail_" + time_data)

    count_time += 1
    tmp = datetime.datetime.now() - tmp_time
    total_time += tmp.total_seconds()

    driver.execute_script("window.history.go(-1)")
    time.sleep(3)

print (total_time)
print (count_time)
print (total_time/count_time)

import runner.pre_processing as pre

pre.runner("dailymail")