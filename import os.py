import os
import glob
import string

class Query:
    def __init__(self, query_id, title, description, narrative):
        self.query_id = query_id
        self.title = title
        self.description = description
        self.narrative = narrative

    def __str__(self):
        return f"Query ID: {self.query_id}, Title: {self.title}"

class QueryCollection:
    def __init__(self):
        self.queries = []

    def add_query(self, query):
        self.queries.append(query)

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
                    description = lines[i + 1].strip()
                elif '<narr>' in line:
                    narrative = ' '.join(lines[i + 1:]).replace('<narr>', '').strip()
            
            if query_id and title and description and narrative:
                query = Query(query_id, title, description, narrative)
                query_coll.add_query(query)
    
    return query_coll

# Example usage:
stop_words = get_stopwords()  # Assuming get_stopwords function is defined
query_file = '/mnt/data/the50Queries.txt'
query_collection = parse_query(stop_words, query_file)

# Output each query
for query in query_collection.queries:
    print(query)
