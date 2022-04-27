import xml.etree.ElementTree as et
import file_io
import re

class Indexer:
    def __init__(self, xml, titles, docs, words):
        root = et.parse(xml).getroot()
        to_return = {}
        pg_maxes = {}
        for page in root:
            pg_id = int(page.find('id').text)
            n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
            words = re.findall(n_regex, page.find('text').text)
            for word in words:
                if word not in to_return.keys():
                    to_return[word] = {}
                    to_return[word][pg_id] = 1
                else:
                    if pg_id not in to_return[word].keys():
                        to_return[word][pg_id] = 1
                    else:
                        to_return[word][pg_id] += 1
                
            [print(to_return)]
            ## need to implement pg_maxes
            ## will eventually call file_io method with dictionary and titles as parameter etc.

            
