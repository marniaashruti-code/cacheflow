import streamlit as st
from cache_engine import get_file_hash, LRUCache
from compression_utils import compress_data
from savings import calculate_savings

st.title("CacheFlow")
st.write("Upload files to see real storage savings from deduplication and compression.")

uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

if uploaded_files:
    seen_hashes = {}
    total_size = 0
    unique_size = 0
    compressed_size = 0
    for f in uploaded_files:
        file_bytes = f.read()
        file_hash = get_file_hash(file_bytes)
        total_size += len(file_bytes)
        if file_hash not in seen_hashes:
            seen_hashes[file_hash] = f.name
            unique_size += len(file_bytes)
            compressed_size += len(compress_data(file_bytes))

    st.metric("Original size", f"{total_size/1024:.1f} KB")
    st.metric("After dedup", f"{unique_size/1024:.1f} KB")
    st.metric("After dedup + compression", f"{compressed_size/1024:.1f} KB")
    saved = total_size - compressed_size
    st.metric("Total saved", f"{saved/1024:.1f} KB ({saved/total_size*100:.1f}%)")

    dollars_saved, kwh_saved = calculate_savings(saved)
    st.write(f"💰 Estimated savings: **${dollars_saved:.6f}/month** in storage costs")
    st.write(f"⚡ Estimated energy saved: **{kwh_saved:.6f} kWh/month**")
    st.caption("Based on AWS S3 standard storage pricing and published data center energy-use estimates. Small per-file, but scales linearly with library size.")

    st.divider()
    st.subheader("Smart Cache Simulation")
    st.write("Upload 3+ different files, then click 'Access' on them to see the cache keep your most-used files fast and bump out the least-used one.")

    if "lru" not in st.session_state:
        st.session_state.lru = LRUCache(capacity=2)
        st.session_state.log = []

    file_names = list(seen_hashes.values())
    chosen = st.selectbox("Pick a file to access", file_names)

    if st.button("Access this file"):
        result = st.session_state.lru.access(chosen)
        st.session_state.log.append(f"{chosen} → {result}")

    st.write("**Currently in fast cache:**", st.session_state.lru.contents())
    st.write("**Access log (most recent first):**")
    for entry in reversed(st.session_state.log):
        st.write("-", entry)