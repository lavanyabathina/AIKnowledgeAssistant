from langchain_huggingface import HuggingFaceEmbeddings
from models.embedded_chunk import EmbeddedChunk
import time

#Get Embedding model
def get_embedding_model():
    embedModel = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedModel

#Generate Embeddings
def generate_embeddings(chunks: List[Document], embedding_model):

    print(f"Generating embeddings for {len(chunks)} chunks")

    texts = [chunk.page_content for chunk in chunks]

    batch_size = 500
    embedded_chunks = []

    start = time.time()

    for i in range(0, len(texts), batch_size):

        print(f"Embedding batch {i//batch_size + 1} "
              f"({i} - {min(i + batch_size, len(texts))})")

        batch_texts = texts[i:i + batch_size]

        batch_vectors = embedding_model.embed_documents(batch_texts)

        for chunk, vector in zip(chunks[i:i + batch_size], batch_vectors):
            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=chunk,
                    embedding=vector
                )
            )

    print(f"Completed in {time.time() - start:.2f} seconds")

    return embedded_chunks
