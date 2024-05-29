
"""Iterator over a collection."""

from bow_coll_inorder_iterator import BowCollInorderIterator

class BowQueryColl:
    """Collection of BOW documents."""

    def __init__(self):
        """Constructor.

        Creates an empty collection."""
        self.queries = {}

    def add_query(self, query):
        """Add a query to the collection."""
        self.queries[query.get_queryid()] = query

    def get_query(self, queryid):
        """Return a query by queryid.

        Will raise a KeyError if there is no query with that ID."""
        return self.queries[queryid]

    def get_queries(self):
        """Get the full list of queries.

        Returns a dictionary, with queryids as keys, and queries as values."""
        return self.queries

    def inorder_iter(self):
        """Return an ordered iterator over the queries.
        
        The iterator will traverse the collection in queryid order.  Modifying
        the collection while iterating over it leads to undefined results.
        Each element is a query; to find the id, call queries.get_queryid()."""
        return BowCollInorderIterator(self)

    def get_num_queries(self):
        """Get the number of queries in the collection."""
        return len(self.queries)

    def __iter__(self):
        """Iterator interface.

        See inorder_iter."""
        return self.inorder_iter()
    
    def get_collection_term_frequency(self):
        """Get the term frequency in the collection."""
        term_freq = {}
        for query in self.queries.values():
            for term in query.get_term_list():
                try:
                    term_freq[term] += query.get_term_count(term)
                except KeyError:
                    term_freq[term] = query.get_term_count(term)
        return term_freq