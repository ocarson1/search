import xml.etree.ElementTree as et
import file_io
import re
import math
import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
STOP_WORDS = set(stopwords.words('english'))

class Indexer:
    
    def __init__(self, xml, titles_file, docs_file, words_file) -> None:
        """Parses through an xml, recording the titles, ids, ranks of each page, and relevancy of each word for each
        page. Writes this information into three files.
        
        Parameters:
        xml -- the xml file to be parsed
        titles_file -- an empty file for ids to titles to be written
        docs_file -- an empty file for ids to pageranks to be written
        words_file -- an empty file for words to ids to relevance to be written"""

        
        root = et.parse(xml).getroot()
        stemmer = PorterStemmer()
        words_to_doc_relv = {}
        doc_max_freqs = {}
        self.weight_dict = {}
        self.ids_to_titles = {}
        self.titles_to_ids = {}
        self.pg_links = {}
        
        for page in root:
            pg_id = int(page.find('id').text)
            title: str = (page.find('title').text)
            title = title.strip()
            self.ids_to_titles.update({pg_id : title})
            self.titles_to_ids.update({title : pg_id})
            self.pg_links[title] = set() #each title maps to a set so that there are no repeated links

            n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            words = re.findall(n_regex, title) + (re.findall(n_regex, page.find('text').text))
            
            for word in words:
                word_lst = [word] # We create this list for the case where the regex finds multiple consecutive words in a link
                
                # if the word is a link, we handle here by adding the name of the link to pg_links, then continuing
                if (re.search('\[\[[^\[]+?\]\]', word) != None): 
                    word = word.strip('[]')
                    link_to = word
                    word_lst = [word]
                    if '|' in word: 
                        link_to = (word.split('|'))[0]
                        word = (word.split('|'))[1]
                    word_lst = re.findall(n_regex, word)
                    if link_to != title:
                        self.pg_links[title].add(link_to)

                for w in word_lst:
                    w = w.lower()
                    stemmer.stem(w)
                    if w in STOP_WORDS: 
                        continue # skips adding stop words to our words_to_doc_relv dictionary

                    # words_to_doc_relv temporarily maps from a word to a document to the word's frequency on that document
                    if w not in words_to_doc_relv.keys():
                        words_to_doc_relv[w] = {}
                        words_to_doc_relv[w][pg_id] = 1
                    else:
                        if pg_id not in words_to_doc_relv[w].keys():
                            words_to_doc_relv[w][pg_id] = 1
                        else:
                            words_to_doc_relv[w][pg_id] += 1
                    if pg_id not in doc_max_freqs:
                        doc_max_freqs[pg_id] = 1
                    elif words_to_doc_relv[w][pg_id] > doc_max_freqs[pg_id]:
                        doc_max_freqs[pg_id] = words_to_doc_relv[w][pg_id]

        # rewrites the value of the inner dictionary with word-document relevance by using TF and IDF calculations.
        # doc_max_freqs is used here to get the aj variable in the formula and to get the total number of words in a document
        for word in words_to_doc_relv:
            for pg_id in words_to_doc_relv[word]:
                words_to_doc_relv[word][pg_id] = (words_to_doc_relv[word][pg_id] / doc_max_freqs[pg_id]) * math.log(len(doc_max_freqs) / len(words_to_doc_relv[word]))           

        self.calculate_weights()
        ids_to_pgranks = self.pagerank()

        file_io.write_title_file(titles_file, self.ids_to_titles)  
        file_io.write_docs_file(docs_file, ids_to_pgranks)  
        file_io.write_words_file(words_file, words_to_doc_relv) 

        

    def calculate_weights(self):
        """Calculates the weight between every page in the xml, determined by links between pages"""

        e = 0.15

        # initializes a default weight between all pages
        for k_title in self.titles_to_ids.keys(): 
            k_id = self.titles_to_ids[k_title]
            self.weight_dict[k_id] = {}
            for j_title in self.titles_to_ids.keys(): 
                j_id = self.titles_to_ids[j_title]
                self.weight_dict[k_id][j_id] = e/len(self.titles_to_ids.keys())

        # creates a dictionary storing the number of links in a page
        id_to_link_number = {}
        for k_id in self.weight_dict.keys():
            k_title = self.ids_to_titles[k_id]
            id_to_link_number[k_id] = 0

            # adds 1 to n_k for each valid link 
            for link_to in self.pg_links[k_title]: 
                if link_to in self.titles_to_ids.keys() and link_to != k_title: 
                    id_to_link_number[k_id] += 1

            # n_k is number of pgs -1 if pg has no links
            if id_to_link_number[k_id] == 0:
                id_to_link_number[k_id] = len(self.ids_to_titles.keys()) - 1
                for other_title in self.titles_to_ids.keys():
                    if other_title != k_title:
                        self.pg_links[k_title].add(other_title)

            # rewrites weights for pages that link to other pages
            for j_id in self.weight_dict[k_id]:
                if self.ids_to_titles[j_id] in self.pg_links[self.ids_to_titles[k_id]]:
                    self.weight_dict[k_id][j_id] = self.weight_dict[k_id][j_id] + (1 - e) * (1/id_to_link_number[k_id])
                
    def pagerank(self):
        """Using the calculated weights between pages, this method calculates the pagerank of every page"""
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
                        next[j] = next[j] + self.weight_dict[k][j] * curr[k]
        return next
            
    def distance(self, x, y):
        """this helper method calculates the Euclidean distance between two vectors"""
        distance = 0
        subtracted = []
        for i, j in zip(x.values(),y.values()):
            subtracted.append((j - i)**2)
        for i in subtracted:
            distance += i
        return math.sqrt(distance)

def main():
    
        if len(sys.argv) - 1 == 4:
            xml = sys.argv[1]
            titles_file = sys.argv[2]
            docs_file = sys.argv[3]
            words_file = sys.argv[4]
            indexer = Indexer(xml, titles_file, docs_file, words_file)
        else: 
            print("Error: incorrect number of arguments")

if __name__ == "__main__":
    main()

        
        
        
            

