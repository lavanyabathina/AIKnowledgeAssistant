from loaders.webdocument_loader import *
from loaders.localdocument_loader import *
from pathlib import Path

def load_documents(dataset_config,directory ):
    """
    loads all files from given directory
    """
    print (f"Loading documents from {directory}")
    documents = []
    directory = Path(directory)

    web_source_directory = dataset_config["web_source_directory"]
    local_source_directory = dataset_config["local_source_directory"]
    web_directory = Path(web_source_directory)
    local_directory = Path(local_source_directory)
    markdown_exists = any(web_directory.rglob("*.md"))
    pdf_exists = any(local_directory.rglob("*.pdf"))
    
    if markdown_exists:
        md_documents=load_markdown_documents(web_source_directory)
        documents.extend(md_documents)
        documents = clean_markdown_documents(documents)
    if pdf_exists:
        pdf_documents = load_pdf_documents(local_source_directory)
        documents.extend(pdf_documents)
    return documents


