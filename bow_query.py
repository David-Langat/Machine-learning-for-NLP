class Query:
    def __init__(self):
        self.terms = {} 

    def get_terms(self):
        return self.terms
    
    def add_term(self, term):
        try:
            self.terms[term] += 1
        except KeyError:  
            self.terms[term] = 1
    