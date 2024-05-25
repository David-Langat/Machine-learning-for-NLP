class BowCollInorderIterator:
    """Iterator over a collection."""

    def __init__(self, coll):
        """Constructor.
        
        Takes the collection we're going to iterator over as sole argument."""
        self.coll = coll
        self.keys = sorted(coll.get_docs().keys())
        self.i = 0

    def __iter__(self):
        """Iterator interface."""
        return self

    def __next__(self):
        """Get next element."""
        if self.i >= len(self.keys):
            raise StopIteration
        doc = self.coll.get_doc(self.keys[self.i])
        self.i += 1
        return doc