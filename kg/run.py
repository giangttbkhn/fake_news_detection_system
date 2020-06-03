from graph.graph import Graph
from os import listdir
from os.path import isfile, join

graph = Graph()
def get_all_sources():
    folders = ['cnn', 'dailymail', 'news_fox']
    files = []
    for folder in folders:
        path = './data/triples/' + folder
        fileFolders = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        files.extend(fileFolders)
    return files

def contribute_graph():
    sources = get_all_sources()
    graph.data_processor.add_source(sources)
    graph.contribute_graph()

def run():
    print("=============================================================================================================\n")
    print("                  Enter any news to detect the fake news and type end to end the program\n")
    print("=============================================================================================================\n")
    while True:
        print("news:")
        news = input()
        if news == 'end':
            break
        graph.detect_fake_news(news)


if __name__ == "__main__":
    # contribute_graph()
    run()



