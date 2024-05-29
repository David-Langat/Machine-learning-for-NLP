class BowQuery:
    def __init__(self,queryid):
        """Constructor."""
        self.terms = {}
        self.queryid = queryid
        self.query_title=''
        self.query_desc=''
        self.query_narr=''

    def get_terms(self):
        """Get the full list of terms."""
        return self.terms

    def get_query_title(self):
        '''Get the query title'''
        return self.query_title
  
    def get_query_desc(self):
        '''Get the query description'''
        return self.query_desc

    def get_query_narr(self):
        '''Get the query narrative'''
        return self.query_narr
    
    def add_term(self, term):
        """Add a term occurrence to the BOW representation."""
        try:
            self.terms[term] += 1
        except KeyError:  
            self.terms[term] = 1

    def get_term_count(self, term):
        """Get the term occurrence count for a term.

        Returns 0 if the term does not appear in the query."""
        try:
            return self.terms[term]
        except KeyError:
            return 0

    def get_term_freq_dict(self):
        """Return dictionary of term:freq pairs."""
        return self.terms

    def get_term_list(self):
        """Get sorted list of all terms occurring in the query."""
        return sorted(self.terms.keys())

    def get_queryid(self):
        """Get the ID of the query."""
        return self.queryid
    
    def get_query_text(self):
        """Get the text of the query."""
        line = self.query_title + ' ' + self.query_desc + ' ' + self.query_narr
        return line
