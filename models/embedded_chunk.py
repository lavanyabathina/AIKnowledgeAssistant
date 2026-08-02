from dataclasses import dataclass
from langchain_core.documents import Document
@dataclass
class EmbeddedChunk:
    chunk : Document
    embedding : List[float]
