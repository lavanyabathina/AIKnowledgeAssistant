from langchain_groq import ChatGroq
import os


def get_groq_llm(model,temperature):
    print("get groq llm")
    llm = ChatGroq(
    model=model,
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
    )
    return llm
