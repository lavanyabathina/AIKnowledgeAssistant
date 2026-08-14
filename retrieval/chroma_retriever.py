import chromadb
from langchain_chroma import Chroma

def get_chroma_retriever(application_config, embedding_model, k=None):
    collection_name = application_config["vector_db"]["collection"]
    vector_db_path = application_config["vector_db"]["path"]
    
    # Use the passed 'k' (candidate_k) if provided by the hybrid retriever, otherwise fallback to config
    top_k = k if k is not None else application_config["retrieval"]["top_k"]

    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=vector_db_path,
        embedding_function=embedding_model
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k" : top_k}
    )

    return retriever