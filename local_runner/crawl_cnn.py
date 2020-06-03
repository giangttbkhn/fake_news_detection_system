from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
import datetime

def count_luanvan(luanvan_results):
    results = luanvan_results.find_elements_by_tag_name("div")

    return len(results)

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/"
pattern_url = "https://edition.cnn.com/"
key_search = "donald trump"
path_save = DIR_PATH + "cnn"
key_search_pattern = key_search.replace(" ", "%20")

pattern_next = "https://edition.cnn.com/search?q=" + key_search_pattern + \
               "&size=10&page=@page@&from=@index@&category=us,politics,world,opinion,health"

options = webdriver.ChromeOptions()
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

now = datetime.datetime.now()

folder_name = str(now).split(" ")[0].replace("-", "_")

path_save_ = path_save + "/" + folder_name

if os.path.isdir(path_save_) == False:
    os.makedirs(path_save_)

page = 2
count_overlap = 0
count_time = 0
total_time = 0
while (1):

    tmp_time  = datetime.datetime.now()
    i = 1
    current_url = driver.current_url

    if count_overlap >= 10:
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
    tmp = tmp.replace("@index@", str((page-1)*10))
    driver.get(tmp)
    page += 1
    time.sleep(3)

print (total_time)
print (count_time)
print (total_time/count_time)

import runner.pre_processing as pre

pre.runner("cnn")