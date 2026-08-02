from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


def load_pdf_documents(source_directory):
    print(f"Loading PDF documents from {source_directory}")

    loader = DirectoryLoader(
        path=source_directory,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    print("PDF documents loaded:", len(documents))

    return documents