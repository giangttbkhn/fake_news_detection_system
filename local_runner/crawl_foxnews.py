from selenium import webdriver
import os
import time
import datetime

def count_luanvan(luanvan_results):
    results = luanvan_results.find_elements_by_tag_name("article")

    return len(results)

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"
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

now = datetime.datetime.now()

folder_name = str(now).split(" ")[0].replace("-", "_")
# folder_name = "2020_05_22"
path_save_ = path_save + "/" + folder_name

if os.path.isdir(path_save_) == False:
    os.makedirs(path_save_)

i = 1
count_overlap = 0

count_time = 0
total_time = 0
while (1):

    tmp_time = datetime.datetime.now()
    if count_overlap >= 10:
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

print (total_time)
print (count_time)
print (total_time/count_time)

import runner.pre_processing as pre

pre.runner("news_fox")