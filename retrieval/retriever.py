from retrieval.chroma_retriever import get_chroma_retriever
from retrieval.hybrid_retriever import get_hybrid_retriever

def get_retriever(application_config, embedding_model):
    # Check if a specific retrieval type is defined (defaulting to standard vector if not)
    retrieval_type = application_config.get("retrieval", {}).get("type", "standard")
    vector_db_type = application_config["vector_db"]["type"]
    
    if retrieval_type == "hybrid":
        print("Getting Hybrid Retriever")
        return get_hybrid_retriever(application_config, embedding_model)

    # Fallback to standard DB retrievers
    elif vector_db_type == "chroma":
        print("Getting Chroma Retriever")
        return get_chroma_retriever(application_config, embedding_model)

    else:
        raise ValueError(
            f"Unsupported vector DB: {vector_db_type}"
        )