import os
import string
import glob
from stemming.porter2 import stem
from bow_doc import BowDoc  # Ensure this module is available and correctly imported
from bow_coll import BowColl  # Ensure this module is available and correctly imported

class Query:
    def __init__(self, query_id, title, description, narrative):
        self.query_id = query_id
        self.title = title
        self.description = description
        self.narrative = narrative

    def __str__(self):
        return (f"Query ID: {self.query_id}\n, Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"Narrative: {self.narrative}\n")

class QueryCollection:
    def __init__(self):
        self.queries = []

    def add_query(self, query):
        self.queries.append(query)

def get_stopwords():
    """Get a list of stopwords."""
    with open('common-english-words.txt', 'r') as stopwords_f:
        stop_words = stopwords_f.read().split(',')
    return stop_words

def parse_documents(stop_words, inputpath):
    print("Parsing documents...")
    bow_coll = BowColl()  # Create an instance of the BowColl class
    os.chdir(inputpath)   # Change working directory to the inputpath variable
    
    for file in glob.glob('*.xml'):  # Iterate through all files with .xml
        document = BowDoc(docid=0)  # Initializing a document object for the current file
        start_end = False  # Variable to signal the end of the document id section
        
        with open(file, 'r') as f:
            for line in f:  # Iterate through each line within the file
                line = line.strip()  # Remove the \n tags in the line
                
                if not start_end:
                    if line.startswith("<newsitem "):
                        for part in line.split():
                            if part.startswith("itemid="):
                                document.docid = part.split("=")[1].split("\"")[1]  # Get the document id and store it as an attribute for the document object
                                break
                    if line.startswith("<text>"):
                        start_end = True
                elif line.startswith("</text>"):
                    break
                else:
                    line = line.replace("<p>", "").replace("</p>", "")
                    line = line.translate(str.maketrans('', '', string.digits)).translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                    line = ' '.join(line.split())
                    
                    for term in line.split():  # Split the line into words
                        document.doc_len += 1
                        term = stem(term.lower())
                        if len(term) > 2 and term not in stop_words:
                            document.add_term(term)  # Add terms into the document object

        document.set_doc_len(document.doc_len)
        bow_coll.add_doc(document)  # Add document to the collection object BowColl
    
    os.chdir('..')
    return bow_coll

def parse_query(stop_words, query_file):
    """Parse a query into a query object then add it to the collection"""
    query_coll = QueryCollection()
    
    with open(query_file, 'r') as file:
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
                query = Query(query_id, title, description, narrative)
                query_coll.add_query(query)
    
    return query_coll

# Example usage:
stop_words = get_stopwords()  # Assuming get_stopwords function is defined
query_file = r"C:\Users\s4021\OneDrive\桌面\Machine-learning-for-NLP\the50Queries.txt"  # Use raw string for Windows path
query_collection = parse_query(stop_words, query_file)

# Output each query
for query in query_collection.queries:
    print(query)
