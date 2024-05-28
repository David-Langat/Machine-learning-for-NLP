import os, string, glob
from stemming.porter2 import stem
from bow_doc import BowDoc
from bow__doc_coll import BowDocColl
from bow_query import BowQuery

def get_stopwords():
    """Get a list of stopwords."""

    stopwords_f = open('common-english-words.txt', 'r', encoding='utf-8')
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()
    return stop_words


def parse_documents(stop_words, inputpath):
    print("Parsing documents...")
    bow_doc_coll = BowDocColl()                            #Create an instance of the BowColl class
    #local variables
    os.chdir(inputpath)                             #change working directory to the inputpath variable
    for file in glob.glob('*.xml'):                 #Iterate through all files with .xml
        document = BowDoc(docid=0)    #Initializing a document object for the current file
        start_end = False                           #Variable to signal the end of the document id section
        for line in open(file, encoding='utf-8'):                     #iterate through each line within the list
            line=line.strip()                       #remove the \n tags in the list
            if(start_end == False):
                if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            document.docid = part.split("=")[1].split("\"")[1]      #get the document id and store it as an attribute for the document object
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
                        document.add_term(term)                     # I add terms into the document object. A term is a stem of a word that has more than 2 characters and is not a common english word.

        #set the doc_len of the document object
        document.set_doc_len(document.doc_len)
        #add document to the collection object Bowcoll
        bow_doc_coll.add_doc(document)  # Call the add_doc method on the instance

    os.chdir('..')
    return bow_doc_coll

def parse_query(query_file, stop_words):
    """Parse a query into a query object then add it to the collection"""
    

    with open(query_file, encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            query_not_end = True
            while query_not_end:
                print(line)
                if line.startswith('</Query>'):
                    query_not_end = False
                    break
                i += 1
                if i < len(lines):
                    line = lines[i].strip().strip('\n')
                else:
                    query_not_end = False
            if not query_not_end:
                  break
                  
                      

            



