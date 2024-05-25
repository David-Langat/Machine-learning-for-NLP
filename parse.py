import os, string, glob
from stemming.porter2 import stem
from bow_doc import BowDoc



def parse_rcv1v2(stop_words, inputpath):
    #local variables
    document_collection = {}                      #A dictonary collection of document objects as values and their ids as keys.
    os.chdir(inputpath)                             #change working directory to the inputpath variable
    for file in glob.glob('*.xml'):                 #Iterate through all files with .xml
        document = BowDoc(docid=0)    #Initializing a document object for the current file
        start_end = False                           #Variable to signal the end of the document id section
        for line in open(file):                     #iterate through each line within the list
            line=line.strip()                       #remove the \n tags in the list
            if(start_end == False):
                if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            document.docId = part.split("=")[1].split("\"")[1]      #get the document id and store it as an attribute for the document object
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
                        
        document_collection[document.docId] = document        
    os.chdir('..')
    return document_collection