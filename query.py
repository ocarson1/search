from numpy import sort
from regex import P
import file_io
import sys
import re 
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer


class Querier: 
    
    def __init__(self, titles_file, docs_file, words_file, is_pg_rank):
        """The querier reads xml information from three files and uses a REPL to print the most relevant pages to a user's query"""
        
        self.ids_to_titles = {}
        self.ids_to_page_ranks = {} 
        self.words_to_doc_relevance ={}
        self.is_pg_rank = is_pg_rank

        file_io.read_title_file(titles_file, self.ids_to_titles)
        file_io.read_docs_file(docs_file, self.ids_to_page_ranks)
        file_io.read_words_file(words_file, self.words_to_doc_relevance)

        self.repl()

    def repl(self):
        """the REPL takes in user input, stems it and removes stop words, then goes through the information read in by the
        file_io and finds the most relevant documents to the input based upon word relevance and optional document pagerank"""
        
        stemmer = PorterStemmer()
        n_regex = '''[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        print("\n** type ':quit' to quit the program **")
        print("\nENTER QUERY:")
        x = input()
        while x != ":quit":
            query_terms = []
            pg_to_score = {}
            input_terms = re.findall(n_regex, x)
            #  stems and removes stop words from the input
            for term in input_terms:
                stemmer.stem(term)
                if term not in STOP_WORDS:
                    query_terms.append(term)

            for word in query_terms:
                if word in self.words_to_doc_relevance.keys():
                    for doc in self.words_to_doc_relevance[word]:
                        if doc not in pg_to_score.keys():
                            if self.is_pg_rank:
                                pg_to_score[doc] = self.words_to_doc_relevance[word][doc] * self.ids_to_page_ranks[doc]
                            else:
                                pg_to_score[doc] = self.words_to_doc_relevance[word][doc]
                        else:
                            if self.is_pg_rank:
                                pg_to_score[doc] += self.words_to_doc_relevance[word][doc] * self.ids_to_page_ranks[doc]
                            else: pg_to_score[doc] += self.words_to_doc_relevance[word][doc]
            print("\nRESULTS:")

            # case in which the query cannot be found in the wiki
            if len(pg_to_score) == 0:
                print("No results found, try another query")
            else:
                sort_pages = sorted(pg_to_score.items(), key=lambda x: x[1], reverse=True)
                if len(sort_pages) < 10:
                    for page in sort_pages:
                        print(self.ids_to_titles[page[0]])
                else:
                    for i in range(0, 11):
                        print(self.ids_to_titles[sort_pages[i][0]])

            print("\nENTER QUERY:")
            x = input() #asks for input again so that the while loop can be repeated or quitted
        
def main():
    if len(sys.argv) != 4 or 5:
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
        Querier(titles_file, docs_file, words_file, is_pg_rank)
    else:
        print("Error: incorrect number of arguments")
    
if __name__ == "__main__":
    main()
        

            




        

