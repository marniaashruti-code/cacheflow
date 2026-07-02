import hashlib

# Rolling hash parameters
WINDOW_SIZE = 16
PRIME = 101
MODULUS = 1024  # Trigger boundary when rolling_hash % MODULUS == 0
MIN_CHUNK = 1024   # 1KB minimum chunk size to avoid tiny chunks
MAX_CHUNK = 16384  # 16KB maximum chunk size to prevent massive chunks

def _rolling_hash_boundaries(data: bytes) -> list:
    """
    Finds variable-sized chunk boundaries using a Rabin-Karp style rolling hash.
    Ensures that insertions/deletions only affect local boundaries (avoids boundary-shift problem).
    """
    boundaries = [0]
    n = len(data)
    if n <= MIN_CHUNK:
        return boundaries

    current_hash = 0
    power = 1
    
    # Precompute (PRIME ^ (WINDOW_SIZE - 1)) % MODULUS
    for _ in range(WINDOW_SIZE - 1):
        power = (power * PRIME) % MODULUS

    # Initialize the hash for the first window
    if n >= WINDOW_SIZE:
        for i in range(WINDOW_SIZE):
            current_hash = (current_hash * PRIME + data[i]) % MODULUS

    last_boundary = 0
    
    # Slide the window across the data
    for i in range(n - WINDOW_SIZE + 1):
        # Check if we have met the minimum chunk requirement
        current_chunk_size = i - last_boundary
        
        if current_chunk_size >= MIN_CHUNK:
            # Trigger boundary on magic pattern or if hitting MAX_CHUNK
            if current_hash == 0 or current_chunk_size >= MAX_CHUNK:
                boundaries.append(i)
                last_boundary = i
        
        # Roll the hash forward to the next byte
        if i < n - WINDOW_SIZE:
            out_byte = data[i]
            in_byte = data[i + WINDOW_SIZE]
            
            # Remove high-order byte, shift left, add low-order byte
            current_hash = (current_hash - (out_byte * power) % MODULUS + MODULUS) % MODULUS
            current_hash = (current_hash * PRIME + in_byte) % MODULUS

    return boundaries

def split_into_chunks(data: bytes) -> list:
    """
    Splits binary data into a list of variable-sized bytes blocks using content-defined chunking.
    """
    boundaries = _rolling_hash_boundaries(data)
    chunks = []
    
    for i in range(len(boundaries)):
        start = boundaries[i]
        end = boundaries[i+1] if i + 1 < len(boundaries) else len(data)
        if start < end:
            chunks.append(data[start:end])
            
    # Fallback to make sure the whole file is chunked if boundaries array was empty/static
    if not chunks and len(data) > 0:
        chunks.append(data)
        
    return chunks

def hash_chunk(chunk_data: bytes) -> str:
    """
    Generates a unique SHA-256 fingerprint for a specific data block.
    """
    return hashlib.sha256(chunk_data).hexdigest()

def analyze_chunks(files_dict: dict) -> dict:
    """
    Processes multiple files, cuts them into variable chunks, finds unique vs duplicate blocks,
    and returns metrics for data reduction analysis.
    
    files_dict: { filename: file_bytes }
    """
    unique_chunks = {}  # { chunk_hash: chunk_size }
    total_chunks_processed = 0
    logical_size = 0
    
    # Tracks which file contains which chunk hashes
    file_manifests = {} # { filename: [hash1, hash2, ...] }
    
    for filename, data in files_dict.items():
        logical_size += len(data)
        chunks = split_into_chunks(data)
        total_chunks_processed += len(chunks)
        
        file_manifests[filename] = []
        for chunk in chunks:
            chash = hash_chunk(chunk)
            file_manifests[filename].append(chash)
            if chash not in unique_chunks:
                unique_chunks[chash] = len(chunk)
                
    physical_size = sum(unique_chunks.values())
    saved_bytes = logical_size - physical_size
    
    # Calculate savings percentage
    savings_pct = (saved_bytes / logical_size * 100) if logical_size > 0 else 0.0
    
    return {
        "logical_size_bytes": logical_size,
        "physical_size_bytes": physical_size,
        "saved_bytes": saved_bytes,
        "savings_percentage": round(savings_pct, 2),
        "total_chunks_processed": total_chunks_processed,
        "unique_chunks_count": len(unique_chunks),
        "file_manifests": file_manifests
