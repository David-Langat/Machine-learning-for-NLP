class BowDoc:
    """Bag-of-words representation of a document.

    The document has an ID, and an iterable list of terms with their
    frequencies."""

    def __init__(self, docid):
        """Constructor.

        Set the ID of the document, and initiate an empty term dictionary.
        Call add_term to add terms to the dictionary."""
        self.docid = docid
        self.terms = {}
        self.doc_len = 0

    def add_term(self, term):
        """Add a term occurrence to the BOW representation.

        This should be called each time the term occurs in the document."""
        try:
            self.terms[term] += 1
        except KeyError:  
            self.terms[term] = 1

    def get_term_count(self, term):
        """Get the term occurrence count for a term.

        Returns 0 if the term does not appear in the document."""
        try:
            return self.terms[term]
        except KeyError:
            return 0

    def get_term_freq_dict(self):
        """Return dictionary of term:freq pairs."""
        return self.terms

    def get_term_list(self):
        """Get sorted list of all terms occurring in the document."""
        return sorted(self.terms.keys())

    def get_docid(self):
        """Get the ID of the document."""
        return self.docid

    def __iter__(self):
        """Return an ordered iterator over term--frequency pairs.

        Each element is a (term, frequency) tuple.  They are iterated
        in term's frequency descending order."""
        return iter(sorted(self.terms.items(), key=lambda x: x[1],reverse=True))
        # Or in term alphabetical order:
        # return iter(sorted(self.terms.iteritems()))

    def get_doc_len(self):
        """Get the number of terms in the document."""
        return self.doc_len

    def set_doc_len(self, doc_len):
        """Set the number of terms in the document."""
        self.doc_len = doc_len
    