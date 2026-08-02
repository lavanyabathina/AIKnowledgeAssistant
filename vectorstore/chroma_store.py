import chromadb
import os
import shutil


def get_collection(vectorDBPath):
    client=chromadb.PersistentClient(
        path=vectorDBPath
    )

    collection= client.get_or_create_collection(name="knowledge_base")
    return collection

#Adding embeddings in batches of 500 embeddings. ChromaDB instance has a maximum batch size of 5461, 
def add_embeddings_to_collection(collection, embedded_chunks, batch_size=5000):

    total = len(embedded_chunks)

    for start in range(0, total, batch_size):
        batch = embedded_chunks[start:start + batch_size]

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for index, item in enumerate(batch, start=start):
            ids.append(f"chunk_{index}")
            documents.append(item.chunk.page_content)
            embeddings.append(item.embedding)
            metadatas.append(item.chunk.metadata)

        print(f"Adding batch {start} - {start + len(batch) - 1}")

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    print("All embeddings added successfully.")


def list_collections(vectorDBPath):

    client = chromadb.PersistentClient(
        path=vectorDBPath
    )

    collections = client.list_collections()
    
    for c in collections:
        print(c.name)
    return collections

def delete_collection(vectorDBPath, collectionName):
    
    client = chromadb.PersistentClient(
        path=vectorDBPath
    )
    if isCollectionExist(vectorDBPath, collectionName) :
        client.delete_collection(collectionName)
        print(f'Collection {collectionName} deleted')
    else:
        print(f"Collection '{collectionName}' does not exist. Nothing to delete.")


def isCollectionExist(vectorDBPath, collectionName):

    client = chromadb.PersistentClient(
        path=vectorDBPath
    )
    collections = client.list_collections()
    
    for c in collections:
        if c.name == collectionName:
            print(f"Collection {collectionName} exists")
            return True
    print(f"Collection {collectionName} doesn't exist")
    return False

def delete_chromadb(vectorDBPath):

    if os.path.exists(vectorDBPath):
        shutil.rmtree(vectorDBPath)
        print(f"ChromaDB deleted from {vectorDBPath}.")
    else:
        print(f"ChromaDB does not exist at {vectorDBPath}.")



