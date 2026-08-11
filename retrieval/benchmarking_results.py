import json
import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from retrieval.chroma_retriever import get_chroma_retriever
from retrieval.hybrid_retriever import get_bm25_retriever
from loaders.load_config import load_config
from processors.embedding_generator import get_embedding_model


application_config = load_config('config/application_config.yaml');
embedding_model = get_embedding_model()

# --- Setup Mock Evaluator Environment (Replace with your actual components) ---
# test_queries = json.load(open("evaluation_set.json"))
test_queries = [
    {"query": "how to create DYNAMIC WEB PAGES in python", "expected_doc_id": "sources/local/pythondocs/Py-tutorial.pdf"},
    {"query": "What are sequence objects in python", "expected_doc_id": "sources/local/pythondocs/python-basics-sample-chapters.pdf"},
    {"query": "Give an example of List comprehension", "expected_doc_id": "sources/local/pythondocs/Python_Loops_Concepts.pdf"},
]

# Assuming you already have these initialized:
candidate_k = 20
chroma_retriever = get_chroma_retriever(application_config, embedding_model, candidate_k)
bm25_retriever = get_bm25_retriever(application_config, candidate_k)
# bm25_retriever.k = 10

# Configure configurations to benchmark
configurations = {
    "Pure Vector": chroma_retriever,
    "RRF (0.5 BM25 / 0.5 Vector)": EnsembleRetriever(retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5]),
    "RRF (0.6 BM25 / 0.4 Vector)": EnsembleRetriever(retrievers=[bm25_retriever, chroma_retriever], weights=[0.6, 0.4]),
    "RRF (0.7 BM25 / 0.3 Vector)": EnsembleRetriever(retrievers=[bm25_retriever, chroma_retriever], weights=[0.7, 0.3]),
}

TOP_K = 5
results_matrix = {}

# --- Benchmarking Engine ---
for config_name, retriever in configurations.items():
    total_mrr = 0
    total_hits = 0
    total_queries = len(test_queries)
    
    for item in test_queries:
        query = item["query"]
        expected_id = item["expected_doc_id"]
        
        # Invoke the current retriever configuration
        retrieved_docs = retriever.invoke(query)[:TOP_K]
        
        # Calculate Hit Rate & Reciprocal Rank
        hit_position = -1
        for rank, doc in enumerate(retrieved_docs, start=1):
            # Make sure your document metadata has an identifier like 'source' or 'id'
            if doc.metadata.get("source") == expected_id:
                hit_position = rank
                break
            else:
                print(f"Query: {query} | Expected: {expected_id} | Retrieved: {doc.metadata.get('source')} at rank {rank}")
                
        if hit_position != -1:
            total_hits += 1
            total_mrr += 1.0 / hit_position
        else:
            total_mrr += 0.0
            
    # Calculate macro-averages
    results_matrix[config_name] = {
        "Hit Rate@5": round(total_hits / total_queries, 3),
        "MRR@5": round(total_mrr / total_queries, 3)
    }

# --- Print Visual Performance Matrix ---
print(f"| Configuration | Hit Rate@{TOP_K} | MRR@{TOP_K} |")
print("|--- |--- |--- |")
for config, metrics in results_matrix.items():
    print(f"| {config} | {metrics['Hit Rate@5']} | {metrics['MRR@5']} |")
