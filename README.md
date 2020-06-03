# Fake_news_detection_using_knowledge_graph
Python implementation of Fake news detection using knowledge graph

## Data Preparation from local

### Installation

1. Clone this repository.
2. Ensure packages are installed using "pip install -r requirements.txt".
3. Put "ChromeDriver" into "chromedriver" folder (you can download "ChromeDriver" from [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/downloads)).
4. Etract "stanford-corenlp.zip" into "api_v2" folder (you can download "stanford-corenlp.zip" from [Stanford CoreNLP – Natural language software](https://stanfordnlp.github.io/CoreNLP/index.html)).

### Dataset

We use a dataset that is crawled from CNN, Dailymail and Foxnews (you can download our triples data from [our drive](https://drive.google.com/drive/folders/19YcTQUnNUyMUMxpQEXM-mIpITGr5Uf0x?fbclid=IwAR3A64hFoTVKBitTgwjpHDY1hYcNi8KD7mJCnEf2Lqr3w_y7RD8diChQ3Ck)).

### To crawl data
```shell
# Crawl from CNN: (path to save raw data: /Fake_news_detection_using_knowledge_graph/cnn)
local_runner/crawl_cnn.py
# Crawl from Dailymail: (path to save raw data: /Fake_news_detection_using_knowledge_graph/dailymail)
local_runner/crawl_dailymail.py
#Crawl from Foxnews: ((path to save to raw data: /Fake_news_detection_using_knowledge_graph/news_fox)
local_runner/crawl_foxnews.py

Notice: processed data is saved in path_to/Fake_news_detection_using_knowledge_graph/processed_data/
```

### Extract triples
Please replace "test1" in the "path" variable with folder name which leads to data  ("processed_data/cnn"|"processed_data/dailymail"|"processed_data/news_fox"). 

```shell
# Running directly from the repository
local_runner/triples_extraction.py

Notice: triples is saved in path_to/Fake_news_detection_using_knowledge_graph/test1.txt

In addition: Stanford CoreNLP ships with a built-in server, which requires only the CoreNLP dependencies. To run this server, simply run:
# Run the server using all jars in the current directory (e.g., the CoreNLP home directory)
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
```
# fake_news_detection_system
