from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents,chunk_size=1000,chunk_overlap=200):

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators = [
        "\n# ",     # H1 headings
        "\n## ",    # H2 headings
        "\n### ",   # H3 headings
        "\n\n",     # Paragraphs
        "\n",       # Lines
        ". ",       # Sentences
        " ",        # Words
        ""          # Characters
        ]

    )

    chunks = splitter.split_documents(documents)
    
    return chunks