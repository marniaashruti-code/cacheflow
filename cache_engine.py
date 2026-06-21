import hashlib

def get_file_hash(file_bytes):
    """Creates a unique fingerprint for a file's content."""
    return hashlib.sha256(file_bytes).hexdigest()

from collections import OrderedDict

class LRUCache:
    """Keeps the most recently accessed files in fast 'hot' storage."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def access(self, key):
        """Simulates accessing a file. Returns 'HIT' if cached, 'MISS' if not."""
        if key in self.cache:
            self.cache.move_to_end(key)
            return "HIT"
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            self.cache[key] = True
            return "MISS"

    def contents(self):
        return list(self.cache.keys())