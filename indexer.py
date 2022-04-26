import xml.etree.ElementTree as et
import re
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
STOP_WORDS = set(stopwords.words('english'))


class Indexer:
    def __init__(self, xml, titles, docs, words):
        root = et.parse('wikis/SmallWiki.xml').getroot()
        to_return = {{}}
        corpus = {}
        doc_max_freqs = {}
        for page in root:
            page_id = int(page.find('id').text)
            title : str = page.find('title').text
            text : str = page.find('text').text
            n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            nltk_stemmer = PorterStemmer()
            tkn_text = re.findall(n_regex, text)
            for word in tkn_text:
                if re.search("\[\[[^\[]+?\]\]", word) != None:
                    print(word) #placeholder - store link (in dict(id -> set of links??)) & remove brackets
                word = word.lower()
                corpus.add(word)
                to_return[word][id] += 1
                if(to_return[word][id]) > doc_max_freqs[id]:
                    doc_max_freqs = to_return[word][id]
            for word in corpus: 
                for pg_id in to_return[word]:
                    to_return[word][pg_id] = to_return[word][pg_id] / doc_max_freqs[pg_id] * math.log(doc_max_freqs.size()/ (to_return[word]).size())



        
        
        
            

