from ast import In
import pytest 
import file_io

from index import * 
from query import * 


def test_page_rank(): 
    i1 = Indexer('wikis/PageRankExample1.xml', 'titles', 'docs', 'words' )   
    pr_dict = i1.pagerank()
    assert sum(pr_dict.values()) == pytest.approx(1)

    i2 = Indexer('wikis/PageRankExample2.xml', 'titles', 'docs', 'words' )   
    pr_dict = i2.pagerank()
    assert sum(pr_dict.values()) == pytest.approx(1)

    i3 = Indexer('wikis/PageRankExample3.xml', 'titles', 'docs', 'words' )   
    pr_dict = i3.pagerank()
    assert sum(pr_dict.values()) == pytest.approx(1)

    i4 = Indexer('wikis/PageRankExample4.xml', 'titles', 'docs', 'words' )   
    pr_dict = i4.pagerank()
    assert sum(pr_dict.values()) == pytest.approx(1)

    i5 = Indexer('wikis/our_test.xml', 'titles', 'docs', 'words' )   
    pr_dict = i5.pagerank()
    assert sum(pr_dict.values()) == pytest.approx(1)

    i6 = Indexer('wikis/no_valid_links.xml', 'titles', 'docs', 'words' )   
    pr_dict = i6.pagerank()
    assert sum(pr_dict.values()) == pytest.approx(1)

def test_tf_idf():
    i1 = Indexer('wikis/test_tf_idf.xml', 'titles', 'docs', 'words')
    words_to_relevancy_1 = {}
    file_io.read_words_file('words', words_to_relevancy_1)
    assert words_to_relevancy_1 == {'page': {1: 0.0, 2: 0.0, 3: 0.0}, '1': {1: 1.0986122886681098}, 'dog': {1: 0.4054651081081644, 2: 0.4054651081081644}, 'bit': {1: 0.4054651081081644, 3: 0.2027325540540822}, 'man': {1: 1.0986122886681098}, '2': {2: 1.0986122886681098}, 'ate': {2: 1.0986122886681098}, 'cheese': {2: 0.4054651081081644, 3: 0.4054651081081644}, '3': {3: 0.5493061443340549}}

    i2 = Indexer('wikis/our_test.xml', 'titles', 'docs', 'words')
    words_to_relevancy_2 = {}
    file_io.read_words_file('words', words_to_relevancy_2)
    assert words_to_relevancy_2 == {'brown': {1: 0.0, 2: 0.0, 3: 0.0}, 'university': {1: 0.4054651081081644, 3: 0.2027325540540822}, 'private': {1: 0.13515503603605478, 3: 0.2027325540540822}, 'ivy': {1: 0.3662040962227032}, 'league': {1: 0.3662040962227032}, 'research': {1: 0.13515503603605478, 3: 0.2027325540540822}, 'huio': {1: 0.3662040962227032}, 'providence': {2: 1.0986122886681098}, 'rhode': {2: 0.7324081924454064}, 'island': {2: 0.7324081924454064}, 'capital': {2: 0.3662040962227032}, 'home': {2: 0.3662040962227032}, 'many': {2: 0.3662040962227032}, 'universities': {2: 0.3662040962227032}, 'including': {2: 0.3662040962227032}, 'college': {2: 0.3662040962227032}, 'nelson': {3: 1.0986122886681098}, 'center': {3: 1.0986122886681098}, 'entrepreneurship': {3: 1.0986122886681098}, 'business': {3: 0.5493061443340549}, 'incubator': {3: 0.5493061443340549}}

    i3 = Indexer('wikis/no_valid_links.xml', 'titles', 'docs', 'words')
    words_to_relevancy_3 = {}
    file_io.read_words_file('words', words_to_relevancy_3)
    assert words_to_relevancy_3 == {'b': {2: 0.6931471805599453}, 'e': {2: 0.6931471805599453}, 'c': {3: 0.6931471805599453}, 'g': {3: 0.6931471805599453}}

test_page_rank()
test_tf_idf()

    