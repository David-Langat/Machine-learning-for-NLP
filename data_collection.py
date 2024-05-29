class DataCollection:
    """A collection of BowDocColl objects."""

    def __init__(self):
        """Constructor.

        Creates an empty collection."""
        self.collections = []

    def add_collection(self, collection):
        """Add a BowDocColl to the collection."""
        self.collections.append(collection)

    def get_collection(self, index):
        """Return a BowDocColl by its index.

        Will raise an IndexError if the index is out of range."""
        return self.collections[index]

    def get_num_collections(self):
        """Get the number of BowDocColl objects in the collection."""
        return len(self.collections)