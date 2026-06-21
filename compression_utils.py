import zlib

def compress_data(file_bytes):
    """Compresses file data and returns the compressed bytes."""
    return zlib.compress(file_bytes, level=9)