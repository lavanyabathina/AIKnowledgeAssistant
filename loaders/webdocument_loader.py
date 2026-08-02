from langchain_community.document_loaders import DirectoryLoader , TextLoader
import re


def load_markdown_documents(directory):
    """
    loads all markdown files from given directory
    """
    print(f"Loading Markdown documents from {directory}")
    loader= DirectoryLoader(

        path=directory,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding":"utf-8"}

    )

    documents = loader.load()
    print("Markdown documents loaded:", len(documents))

    
    return documents

#def extract_metadata():


def clean_markdown_documents(documents):
    print(f"Cleaning markdown documents")
    for doc in documents:
       markdown= doc.page_content
       #extract_metadata()
       markdown = re.sub(r'!\[.*?\]\(.*?\)', '', markdown)

       markdown = re.sub(
        r'\[(.*?)\]\((.*?)\)',
        r'\1',
        markdown
       )

       #markdown = remove_noise(markdown)

       markdown = re.sub(r'\n{3,}', '\n\n', markdown)
       doc.page_content = markdown
    return documents