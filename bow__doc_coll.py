
"""Iterator over a collection."""

from bow_coll_inorder_iterator import BowCollInorderIterator

class BowDocColl:
    """Collection of BOW documents."""

    def __init__(self):
        """Constructor.

        Creates an empty collection."""
        self.docs = {}

    def add_doc(self, doc):
        """Add a document to the collection."""
        self.docs[doc.get_docid()] = doc

    def get_doc(self, docid):
        """Return a document by docid.

        Will raise a KeyError if there is no document with that ID."""
        return self.docs[docid]

    def get_docs(self):
        """Get the full list of documents.

        Returns a dictionary, with docids as keys, and docs as values."""
        return self.docs

    def inorder_iter(self):
        """Return an ordered iterator over the documents.
        
        The iterator will traverse the collection in docid order.  Modifying
        the collection while iterating over it leads to undefined results.
        Each element is a document; to find the id, call doc.get_docid()."""
        return BowCollInorderIterator(self)

    def get_num_docs(self):
        """Get the number of documents in the collection."""
        return len(self.docs)

    def __iter__(self):
        """Iterator interface.

        See inorder_iter."""
        return self.inorder_iter()
    
    def get_collection_term_frequency(self):
        """Get the term frequency in the collection."""
        term_freq = {}
        for doc in self.docs.values():
            for term in doc.get_term_list():
                try:
                    term_freq[term] += doc.get_term_count(term)
                except KeyError:
                    term_freq[term] = doc.get_term_count(term)
        return term_freq