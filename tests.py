from ast import In
import pytest 

from index import * 
from query import * 

def test_page_rank(): 
    i1 = Indexer('wikis\PageRankExample1.xml.xml', 'titles', 'docs', 'words' )   
    pr_dict = i1.pagerank()
    assert sum(pr_dict.values()) == 1

    i2 = Indexer('wikis\PageRankExample2.xml', 'titles', 'docs', 'words' )   
    pr_dict = i2.pagerank()
    assert sum(pr_dict.values()) == 1

    i3 = Indexer('wikis\PageRankExample3.xml', 'titles', 'docs', 'words' )   
    pr_dict = i3.pagerank()
    assert sum(pr_dict.values()) == 1

    i4 = Indexer('wikis\PageRankExample4.xml', 'titles', 'docs', 'words' )   
    pr_dict = i4.pagerank()
    assert sum(pr_dict.values()) == 1

    i5 = Indexer('wikis\our_test.xml', 'titles', 'docs', 'words' )   
    pr_dict = i5.pagerank()
    assert sum(pr_dict.values()) == 1

    