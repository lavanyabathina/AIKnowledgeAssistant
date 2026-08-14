import sys
from pathlib import Path

# Ensure project root is on sys.path so local packages can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loaders.load_config import load_config
from loaders.webdocument_loader import load_markdown_documents, clean_markdown_documents
from loaders.webdocument_generator import create_dataset_from_web
import asyncio
from loaders.localdocument_loader import load_pdf_documents
from processors.document_chunker import chunk_documents
from processors.embedding_generator import get_embedding_model, generate_embeddings
from vectorstore.chroma_store import get_collection
import chromadb
from pathlib import Path
import time


def index_selected_datasets(dataset_names):
    dataset_config = load_config('config/dataset_config.yaml')
    app_config = load_config('config/application_config.yaml')

    vector_db_path = app_config["vector_db"]["path"]
    # Use the existing shared collection name from the project (`knowledge_base`)
    collection = get_collection(vector_db_path)
    # record collection name for logging
    collection_name = getattr(collection, 'name', 'knowledge_base')

    all_documents = []

    for ds in dataset_config.get("datasets", []):
        if ds.get("name") not in dataset_names:
            continue

        print(f"Processing dataset: {ds.get('name')}")

        if ds.get("type") == "web":
            source_dir = Path(dataset_config.get("web_source_directory", "./sources/web")) / ds.get("name")
            md_exists = source_dir.exists() and any(source_dir.rglob("*.md"))
            if not md_exists:
                print(f"Web source directory {source_dir} missing or empty — downloading with crawler")
                try:
                    asyncio.run(create_dataset_from_web(ds.get('name'), ds.get('path')))
                except Exception as e:
                    print(f"Download failed for {ds.get('name')}: {e}")
            # reload existence after possible download
            if source_dir.exists() and any(source_dir.rglob("*.md")):
                docs = load_markdown_documents(str(source_dir))
                docs = clean_markdown_documents(docs)
                # tag each document with its source dataset name for later id-prefixing
                for d in docs:
                    if not getattr(d, 'metadata', None):
                        d.metadata = {}
                    d.metadata['dataset'] = ds.get('name')
                    d.metadata['source_path'] = str(source_dir)
                all_documents.extend(docs)
            else:
                print(f"Web source directory {source_dir} does not exist after attempted download. Skipping.")

        elif ds.get("type") == "local":
            # prefer markdown files in the configured path, else try PDFs
            local_path = Path(ds.get("path"))
            if local_path.exists():
                md_docs = []
                try:
                    md_docs = load_markdown_documents(str(local_path))
                except Exception:
                    md_docs = []

                if md_docs:
                    for d in md_docs:
                        if not getattr(d, 'metadata', None):
                            d.metadata = {}
                        d.metadata['dataset'] = ds.get('name')
                        d.metadata['source_path'] = str(local_path)
                    all_documents.extend(md_docs)
                else:
                    pdf_docs = load_pdf_documents(str(local_path))
                    for d in pdf_docs:
                        if not getattr(d, 'metadata', None):
                            d.metadata = {}
                        d.metadata['dataset'] = ds.get('name')
                        d.metadata['source_path'] = str(local_path)
                    all_documents.extend(pdf_docs)
            else:
                print(f"Local dataset path {local_path} does not exist. Skipping.")

    if not all_documents:
        print("No documents found for the selected datasets. Exiting.")
        return

    chunk_size = app_config.get("chunking", {}).get("chunk_size", 1000)
    chunk_overlap = app_config.get("chunking", {}).get("chunk_overlap", 200)

    chunks = chunk_documents(all_documents, chunk_size, chunk_overlap)
    print(f"Total chunks to embed: {len(chunks)}")

    embedding_model = get_embedding_model()
    embedded_chunks = generate_embeddings(chunks, embedding_model)

    # Add embeddings with stable, dataset-prefixed ids to avoid collisions
    batch_size = 500
    total = len(embedded_chunks)
    for start in range(0, total, batch_size):
        batch = embedded_chunks[start:start + batch_size]
        ids = []
        documents = []
        embeddings = []
        metadatas = []
        for i, item in enumerate(batch, start=start):
            ds_name = item.chunk.metadata.get('dataset', 'unknown') if getattr(item.chunk, 'metadata', None) else 'unknown'
            ids.append(f"{ds_name}_chunk_{i}")
            documents.append(item.chunk.page_content)
            embeddings.append(item.embedding)
            metadatas.append(item.chunk.metadata)

        print(f"Adding batch {start} - {start + len(batch) - 1} to collection {collection_name}")
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    print(f"Finished indexing datasets into collection: {collection_name}")


if __name__ == '__main__':
    # change the dataset names here if you want different ones
    datasets_to_index = ["java"]#, "python"]
    start = time.time()
    index_selected_datasets(datasets_to_index)
    print(f"Completed in {time.time() - start:.2f}s")
