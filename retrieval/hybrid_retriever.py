from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document

from retrieval.chroma_retriever import get_chroma_retriever
from vectorstore.chroma_store import get_collection


class HybridRetriever:
    def __init__(self, ensemble_retriever, final_k=None):
        self.ensemble_retriever = ensemble_retriever
        self.final_k = final_k

    def invoke(self, query, **kwargs):
        docs = self.ensemble_retriever.invoke(query, **kwargs)
        return docs if self.final_k is None else docs[: self.final_k]

    async def ainvoke(self, query, **kwargs):
        docs = await self.ensemble_retriever.ainvoke(query, **kwargs)
        return docs if self.final_k is None else docs[: self.final_k]


def get_bm25_retriever(application_config, k):
    vector_db_path = application_config["vector_db"]["path"]
    collection = get_collection(vector_db_path)
    result = collection.get(include=["documents", "metadatas"])

    documents = result.get("documents", []) or []
    metadatas = result.get("metadatas", []) or [{} for _ in documents]

    if not documents:
        raise ValueError("No documents available in Chroma collection for BM25 retriever.")

    bm25_retriever = BM25Retriever.from_texts(
        texts=documents,
        metadatas=metadatas,
        k=k,
    )
    return bm25_retriever


def get_hybrid_retriever(application_config, embedding_model):
    candidate_k = application_config["retrieval"].get("hybrid_candidate_k", 20)
    final_k = application_config["retrieval"]["top_k"]
    weights = application_config["retrieval"].get("hybrid_weights", [0.6, 0.4])

    if len(weights) != 2:
        raise ValueError("hybrid_weights must be a list of two floats: [bm25_weight, chroma_weight].")

    bm25_retriever = get_bm25_retriever(application_config, candidate_k)
    chroma_retriever = get_chroma_retriever(application_config, embedding_model, candidate_k)

    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, chroma_retriever],
        weights=weights,
    )

    return HybridRetriever(ensemble_retriever, final_k=final_k)

