from retrieval.chroma_retriever import get_chroma_retriever

def get_retriever(application_config , embedding_model):
    vector_db_type = application_config["vector_db"]["type"]
    if vector_db_type == "chroma":
        print("Getting Chroma Retriever")
        return get_chroma_retriever(application_config , embedding_model)

    else:
        raise ValueError(
            f"Unsupported vector DB: {vector_db_type}"
        )