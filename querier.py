from regex import P
import file_io
import sys
import re 
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer


class Querier: 
    
          
    
    def __init__(self, titles_file, docs_file, words_file, is_pg_rank):
        
        self.ids_to_titles = {}
        self.ids_to_page_ranks = {} 
        self.words_to_doc_relevance ={}

        file_io.read_title_file(titles_file, self.ids_to_titles)
        file_io.read_docs_file(docs_file, self.ids_to_page_ranks)
        file_io.read_words_file(words_file, self.words_to_doc_relevance)

        self.query_terms = []
        self.repl()


    


    def repl(self): 
        stemmer = PorterStemmer()
        n_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        while input() != ":quit": 
            print("Enter Query")
            input_terms =  re.findall(n_regex, input())
            for term in input_terms: 
                stemmer.stem(term)
                if term not in STOP_WORDS: 
                    self.query_terms.append(term)
            
        


def main(self): 
    if(sys.argv[1] == "--pagerank"): 
        is_pg_rank = True
        titles_file = sys.argv[2]
        docs_file = sys.argv[3]
        words_file = sys.argv[4]
    else:
        titles_file = sys.argv[1]
        docs_file = sys.argv[2]
        words_file = sys.argv[3]
        is_pg_rank = False
    q = Querier(titles_file, docs_file, words_file, is_pg_rank)
    
if __name__ == "__main__":
    main()
        

            




        

