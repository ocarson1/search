from os import link
import xml.etree.ElementTree as et
import file_io
import re
import math
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer



class Indexer:

    def __init__(self, xml, titles_file, docs_file, words_file):
        root = et.parse(xml).getroot()
        to_return = {}
        doc_max_freqs = {}
        self.weight_dict = {}
        stemmer = PorterStemmer()
        self.ids_to_titles = {}
        self.titles_to_ids = {}
        #ids_to_pgrank = {}
        self.pg_links = {}
        

        for page in root:
            pg_id = int(page.find('id').text)
            title: str = (page.find('title').text)
            title = title.strip()
            self.ids_to_titles.update({pg_id : title})
            self.titles_to_ids.update({title : pg_id})

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
                    if link_to != title:
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

        self.calculate_weights()
        ids_to_pgranks = self.pagerank()
        #print(ids_to_pgranks)

        file_io.write_title_file(titles_file, self.ids_to_titles)  
        file_io.write_docs_file(docs_file, ids_to_pgranks)  
        file_io.write_words_file(words_file, to_return) 

        

    def calculate_weights(self):
        #weights = [[0 for i in range(0, len(self.titles_to_ids) - 1)] for j in range(0, len(self.titles_to_ids) - 1)]
        for title in self.titles_to_ids.keys(): 
            pg_id = self.titles_to_ids[title]
            self.weight_dict[pg_id] = {}
            ##
            for title in self.titles_to_ids.keys(): 
                other_id = self.titles_to_ids[title]
                self.weight_dict[pg_id][other_id] = 0.15/len(self.titles_to_ids.keys())
        
            ##
            
      ##      if title not in self.pg_links:
        ##        for other_pg_id in self.ids_to_titles.keys(): 
         ##           if self.ids_to_titles[other_pg_id] != title:
          ##              self.weight_dict[pg_id][other_pg_id] = 0
       ##     else: 
       ##         for link_to in self.pg_links[title]: 
        ##            link_to_id = self.titles_to_ids[link_to]
           ##        if link_to in self.titles_to_ids.keys() and link_to != title: 
                   ##     self.weight_dict[pg_id][link_to_id] = 0
##
        for k_id in self.weight_dict.keys(): #maybe we can combine this with the first loop?
            if self.ids_to_titles[k_id] not in self.pg_links.keys():
                #print("no links")
                for other_id in self.weight_dict.keys():
                    if other_id != k_id:
                        self.weight_dict[k_id][other_id] += (1 - 0.15) * (1/ (len(self.titles_to_ids.keys()) - 1))
            else:
                #print("links")
                for other_id in self.weight_dict[k_id]:              
                    if self.ids_to_titles[other_id] in self.pg_links[self.ids_to_titles[k_id]]:
                        self.weight_dict[k_id][other_id] += (1 - 0.15) * (1/len(self.pg_links[self.ids_to_titles[k_id]]))
                     #switch weight dict to the other one

    
            
        #print(self.weight_dict)

    def pagerank(self):
        delta = .001
        curr = {}
        next = {}
        for pg_id in self.ids_to_titles.keys():
            curr.update({pg_id : 0})
            next.update({pg_id : 1 / len(self.ids_to_titles)})
        while self.distance(curr, next) > delta:
            curr = next.copy()
            for j in self.ids_to_titles.keys():
                next[j] = 0
                for k in self.ids_to_titles.keys():
                    if j in self.weight_dict[k]:
                        next[j] = next[j] + self.weight_dict[k][j] * curr[k]
        return next
        #print(next)
            

    def distance(self, x, y):
        distance = 0
        subtracted = []
        for i, j in zip(x.values(),y.values()):
            subtracted.append((j - i)**2)
        for i in subtracted:
            distance += i
        return math.sqrt(distance)



        
        
        
            

