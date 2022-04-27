import xml.etree.ElementTree as et
import file_io
import re
import math
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

class Indexer:

    def __init__(self, xml, titles, docs, words):
        root = et.parse(xml).getroot()
        to_return = {}
        doc_max_freqs = {}
        self.weight_dict = {}

        for page in root:
            pg_id = int(page.find('id').text)
            title: str = (page.find('title').text)
            n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            words = re.findall(n_regex, title) + (re.findall(n_regex, page.find('text').text)) #Note: currently includes numbers. not sure if issue or not but handout says it is up to our own discretion
            print(words)
            for word in words:
                word_lst = [word]

                if (re.search('\[\[[^\[]+?\]\]', word) != None): 
                    word.strip('[]')
                    link_to = word
                    word_lst = [word]
                    if '|' in word: 
                        link_to = (word.split('|'))[0]
                        word = (word.split('|'))[1]
                        word_lst = re.findall(n_regex, word)
                    self.weight_dict[title][link_to] = None

                for w in word_lst:
                    w = w.lower()
                    if w in STOP_WORDS:
                        continue
                    if w not in to_return.keys():
                        to_return[w] = {}
                        to_return[w][pg_id] = 1
                    else:
                        if pg_id not in to_return[w].keys():
                            to_return[w][pg_id] = 1
                        else:
                            to_return[w][pg_id] += 1
                    if pg_id not in doc_max_freqs:
                        doc_max_freqs[pg_id] = 1
                    elif to_return[w][pg_id] > doc_max_freqs[pg_id]:
                        doc_max_freqs[pg_id] = to_return[w][pg_id]
        print(to_return)
        for word in to_return:
            for pg_id in to_return[word]:
                to_return[word][pg_id] = (to_return[word][pg_id] / doc_max_freqs[pg_id]) * math.log(len(doc_max_freqs) / len(to_return[word]))                
        print(to_return)
        print(doc_max_freqs)


    def weightCalculator(self, j_id : int, k_id : int): 
        for k_title in self.weight_dict: