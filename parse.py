import os, string, glob
from stemming.porter2 import stem
from bow_doc import BowDoc
from bow__doc_coll import BowDocColl
from bow_query_coll import BowQueryColl
from bow_query import BowQuery
from data_collection import DataCollection

def get_stopwords():
    """Get a list of stopwords."""

    stopwords_f = open('common-english-words.txt', 'r', encoding='utf-8')
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()
    return stop_words


def parse_documents(stop_words, inputpath):
    '''Parse the documents in the given path and return the collection of documents.'''
    print("Parsing documents...")
    data_collection = DataCollection()                            #Create an instance of the BowColl class
    #local variables
    os.chdir(inputpath) 
    print('New collection')                          
    for folder in os.listdir(): 
        os.chdir( os.getcwd() + f'/{folder}')
        bow_doc_coll = BowDocColl()                 
        for file in glob.glob('*.xml'):                 #Iterate through all files with .xml
            document = BowDoc(docid=0)    #Initializing a document object for the current file
            start_end = False                           #Variable to signal the end of the document id section
            for line in open(file, encoding='utf-8'):                     #iterate through each line within the list
                line=line.strip()                       #remove the \n tags in the list
                if(start_end == False):
                    if line.startswith("<newsitem "):
                        for part in line.split():
                            if part.startswith("itemid="):
                                document.docid = int(part.split("=")[1].split("\"")[1])      #get the document id and store it as an attribute for the document object
                                break 
                    if line.startswith("<text>"):
                        start_end = True
                elif line.startswith("</text>"):
                    break
                else:
                    line = line.replace("<p>", "").replace("</p>", "")
                    line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                    line = line.replace("\\s+", " ")
                    for term in line.split():                      #I split the line into words. A word is a sequence of characters terminated by a whitespace or punctuation.
                        document.doc_len = document.doc_len + 1
                        term = stem(term.lower())
                        if len(term) > 2 and term not in stop_words: 
                            document.add_term(term) 
            #add document to the collection object Bowcoll
            bow_doc_coll.add_doc(document) 
            #set the doc_len of the document object
            document.set_doc_len(document.doc_len)
        data_collection.add_collection(bow_doc_coll)
        os.chdir('..')

    os.chdir('..')
    return data_collection

def parse_query(stop_words, query_file):
    """Parse a query into a query object then add it to the collection"""
    query_coll = BowQueryColl()
    with open(query_file, 'r', encoding='utf-8') as file:
        content = file.read().split('</Query>')
        
        for query_block in content:
            query_block = query_block.strip()
            if not query_block:
                continue
            
            query_id = None
            title = None
            description = None
            narrative = None
            
            lines = query_block.split('\n')
            for i, line in enumerate(lines):
                if '<num>' in line:
                    query_id = line.split(': ')[1].strip().replace('R', '')
                elif '<title>' in line:
                    title = line.split('<title>')[1].strip()
                elif '<desc>' in line:
                    description = ' '.join(lines[i + 1:]).split('<narr>')[0].strip().replace('<desc>', '').replace('Description:', '').strip()
                elif '<narr>' in line:
                    narrative = ' '.join(lines[i + 1:]).replace('<narr>', '').replace('Narrative:', '').strip()
            
            if query_id and title and description and narrative:
                query = BowQuery(queryid=0)  # Fix: Changed argument name from 'query_id' to 'queryid'
                query.queryid = int(query_id)
                query.query_title = title
                query.query_desc = description
                query.query_narr = narrative
                query_coll.add_query(query)
                #take the query text and store as query_text variable for parsing
                query_text = query.get_query_title()
                query_text = query_text.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                query_text = query_text.replace("\\s+", " ")
                for term in query_text.split():                      
                    term = stem(term.lower())
                    if len(term) > 2 and term not in stop_words:
                        query.add_term(term)

    
    return query_coll