import streamlit as st
from cache_engine import LRUCache
from compression_utils import compress_data
from savings import calculate_savings
from chunk_dedup import analyze_chunks  # <--- This connects your new smart engine!

st.title("CacheFlow")
st.write("Upload files to see real storage savings from content-defined chunk deduplication and compression.")

uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

if uploaded_files:
    # 1. Structure the files for the chunk engine
    files_dict = {}
    total_size = 0
    compressed_size = 0
    
    for f in uploaded_files:
        file_bytes = f.read()
        files_dict[f.name] = file_bytes
        total_size += len(file_bytes)
        # Compress unique files as a secondary step
        compressed_size += len(compress_data(file_bytes))

    # 2. Run the smart content-defined chunking engine
    analysis = analyze_chunks(files_dict)
    unique_size = analysis["physical_size_bytes"]
    
    # Adjust compression estimates based on the unique data remaining
    savings_factor = unique_size / total_size if total_size > 0 else 1
    final_compressed_size = compressed_size * savings_factor

    # 3. Display Metrics
    st.metric("Original size", f"{total_size/1024:.1f} KB")
    st.metric("After chunk dedup (catches partial edits)", f"{unique_size/1024:.1f} KB")
    st.metric("After chunk dedup + compression", f"{final_compressed_size/1024:.1f} KB")
    
    saved = total_size - final_compressed_size
    st.metric("Total saved", f"{saved/1024:.1f} KB ({saved/total_size*100:.1f}%)")

    dollars_saved, kwh_saved = calculate_savings(saved)
    st.write(f"💰 Estimated savings: **${dollars_saved:.6f}/month** in storage costs")
    st.write(f"⚡ Estimated energy saved: **{kwh_saved:.6f} kWh/month**")
    st.caption("Based on AWS S3 standard storage pricing and published data center energy-use estimates.")

    st.divider()
    st.subheader("Smart Cache Simulation")
    st.write("Upload 3+ different files, then click 'Access' on them to see the cache keep your most-used files fast and bump out the least-used one.")

    if "lru" not in st.session_state:
        st.session_state.lru = LRUCache(capacity=2)
        st.session_state.log = []

    file_names = list(files_dict.keys())
    chosen = st.selectbox("Pick a file to access", file_names)

    if st.button("Access this file"):
        result = st.session_state.lru.access(chosen)
        st.session_state.log.append(f"{chosen} → {result}")

    st.write("**Currently in fast cache:**", st.session_state.lru.contents())
    st.write("**Access log (most recent first):**")
    for entry in reversed(st.session_state.log):
        st.write("-", entry)
