Group members: Efia Awuah and Owen Carson

Known bugs: N/A 

Instructions of use: 
In your terminal, navigate to the project folder 

Input the following command with the wiki you intend to be searching as the XML filepath
python3 index.py <XML filepath> <titles filepath> <docs filepath> <words filepath>

Input the following command, including --pagerank in the given position if you would like 
pagerank to influence the order of your results
python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>

You will be prompted to 'ENTER QUERY' . Type in your query. To exit the program, type :quit 
The program will output up to the top 10 most relevant titles for your query. If no results are found, 
you will receive the error message "No results found, try another query 


Description of how pieces of program fit together
The program consists of 3 files 
- index.py 
- query.py 
- file_io.py, which reads and writes to words, docs and titles 

The indexer parses an xml file constaining the wiki to be queried. It calculates the relevance that each 
document has to each word in the corpus, as well as the pagerank ranking of each document in the wiki. 
This information is written (via file_io) to the words and docs files, which are used by the querier to determine the most 
relevant documents given a query. A mapping of document ids to titles is written to the titles file, so that
the querier can associate document ids to titles. 
Given this information (through the use of file_io), and a query consisting of one or more terms, the querier calculates the 

The indexer and querier do not directly share data; instead, data is transfered by file_io, which reads and 
writes to the docs, words and titles files. 

Description of Testing Process 

Unit tests 
For the indexer, we ran unit tests:
- to test the functioning of our xml parsing, and tf and idf calculations, which were all integrated
into one method for efficiency. Since this method did not have a return, and instead edited a global variable 
(our datastructure), we tested this method using print lines, and ensured each step of the calculation was 
correct before proceeding 

- to test that the pagerank method was calculating ranks correctly. We checked that all pageranks added up to 1.0
for every case 

For the querier, we ran unit tests to test the results output

System tests
In order to test our REPL, and the functioning of the system as a whole, we ran system
tests using custom xml wikis, including those containing various edge cases (documents
that did not link to anything, documents that only linked to invalid documents)



