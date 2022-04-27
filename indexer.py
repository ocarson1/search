from os import link
import xml.etree.ElementTree as et
import file_io
import re
import math
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer



class Indexer:

    def __init__(self, xml, titles, docs, words):
        root = et.parse(xml).getroot()
        to_return = {}
        doc_max_freqs = {}
        self.weight_dict = {}
        stemmer = PorterStemmer()
        ids_to_titles = {}
        titles_to_ids = {}
        ids_to_pgrank = {}
        self.pg_links = {}
        weight_dict = {}
        

        for page in root:
            pg_id = int(page.find('id').text)
            title: str = (page.find('title').text)
            title = title.strip()
            ids_to_titles.update({pg_id : title})
            titles_to_ids.update({title : pg_id})

            n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            words = re.findall(n_regex, title) + (re.findall(n_regex, page.find('text').text)) #Note: currently includes numbers. not sure if issue or not but handout says it is up to our own discretion
            for word in words:

                word_lst = [word] 

                if (re.search('\[\[[^\[]+?\]\]', word) != None): 
                    word = word.strip('[]')
                    link_to = word
                    word_lst = [word]
                    if '|' in word: 
                        link_to = (word.split('|'))[0]
                        word = (word.split('|'))[1]
                    word_lst = re.findall(n_regex, word) 
                    if title not in self.pg_links.keys():
                        self.pg_links[title] = set()
                        self.pg_links[title].add(link_to)
                    else:
                        self.pg_links[title].add(link_to)

                for w in word_lst:
                    w = w.lower()
                    stemmer.stem(w)
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

        for word in to_return:
            for pg_id in to_return[word]:
                to_return[word][pg_id] = (to_return[word][pg_id] / doc_max_freqs[pg_id]) * math.log(len(doc_max_freqs) / len(to_return[word]))                
       
        for title in titles_to_ids.keys(): 
            pg_id = titles_to_ids[title]
            weight_dict[pg_id] = {}
            
            if title not in self.pg_links:
                for other_pg_id in ids_to_titles.keys(): 
                    if ids_to_titles[other_pg_id] != title:
                        weight_dict[pg_id][other_pg_id] = 0
            else: 
                for link_to in self.pg_links[title]: 
                    link_to_id = titles_to_ids[link_to]
                    if link_to in titles_to_ids.keys() and link_to != title: 
                        weight_dict[pg_id][link_to_id] = 0 

        for k_id in weight_dict: 
            for j_id in weight_dict[k_id]: 
                weight_dict[k_id][j_id] = 0.15/len(weight_dict.keys()) + (1 - 0.15) * (1/len(weight_dict[k_id]))

            
        print(weight_dict)




    
            





            ## need to implement pg_maxes
            ## will eventually call file_io method with dictionary and titles as parameter etc.



        
        
        
            

