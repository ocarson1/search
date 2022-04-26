import xml.etree.ElementTree as et

class Indexer:
    def __init__(self, xml, titles, docs, words):
        root = et.parse('wikis/SmallWiki.xml').getroot()
        to_return = {{}}
        for page in root:
            page_id = int(page.find('id').text)
            
