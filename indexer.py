import xml.etree.ElementTree as et
import file_io
import re
import math

class Indexer:
    def __init__(self, xml, titles, docs, words):
        root = et.parse(xml).getroot()
        to_return = {}
        doc_max_freqs = {}
        for page in root:
            pg_id = int(page.find('id').text)
            title: str = (page.find('title').text)
            n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            words = re.findall(n_regex, title) + (re.findall(n_regex, page.find('text').text)) #Note: currently includes numbers. not sure if issue or not but handout says it is up to our own discretion
            for word in words:
                word = word.lower()
                if word not in to_return.keys():
                    to_return[word] = {}
                    to_return[word][pg_id] = 1
                else:
                    if pg_id not in to_return[word].keys():
                        to_return[word][pg_id] = 1
                    else:
                        to_return[word][pg_id] += 1
                if pg_id not in doc_max_freqs:
                    doc_max_freqs[pg_id] = 1
                elif to_return[word][pg_id] > doc_max_freqs[pg_id]:
                    doc_max_freqs[pg_id] = to_return[word][pg_id]
        print(to_return)
        for word in to_return:
            for pg_id in to_return[word]:
                to_return[word][pg_id] = (to_return[word][pg_id] / doc_max_freqs[pg_id]) * math.log(len(doc_max_freqs) / len(to_return[word]))
                print(len)
                
        print(to_return)
        print(doc_max_freqs)

            ## need to implement pg_maxes
            ## will eventually call file_io method with dictionary and titles as parameter etc.

            

