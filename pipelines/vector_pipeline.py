from processors.document_chunker import *
from processors.embedding_generator import *
from vectorstore.chroma_store import *
from loaders.document_loader import *
#from loaders.webdocument_loader import *

def build_vector_db(dataset_config, application_config):
    
    #Load Markdown files from dataset source
    source_directory = dataset_config["source_directory"]
    
    documents=load_documents(dataset_config,source_directory)
   # documents=load_markdown_documents(source_directory)
    
    #Clean loaded markdown documents
    #documents = clean_markdown_documents(documents)

    #Chunk loaded documents  
    chunk_size = application_config["chunking"]["chunk_size"]
    chunk_overlap = application_config["chunking"]["chunk_overlap"]

    
    chunks=chunk_documents(documents,chunk_size,chunk_overlap)
    print("Length of chunks:",len(chunks))
        

    #Print first 5 chunks to review chunking
    for i, chunk in enumerate(chunks[:5]):
        print(f"Chunk {i}")
        print(chunk.metadata)
        print(chunk.page_content)
        print("-" * 50)
    
    #generate embeddings
    print("Generating embeddings")
    embedding_model = get_embedding_model()
    embedded_chunks=generate_embeddings(chunks,embedding_model)
    print("Successfully generated embeddings.")

    #Saving embeddings to  vectorDB
    vectorDBPath = application_config["vector_db"]["path"]
    print("Adding embeddings to collection")
    collection=get_collection(vectorDBPath)
    add_embeddings_to_collection(collection,embedded_chunks,5000)
    print("Successfully added embeddings to ChromaDB collection")

