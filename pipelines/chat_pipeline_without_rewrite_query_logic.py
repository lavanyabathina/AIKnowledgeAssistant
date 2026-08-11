from retrieval.retriever import get_retriever
from processors.embedding_generator import *
from llm.llm_factory import *
from chat.chat_prompt import chat_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


def ask_question(application_config , retriever, question,chat_history,rag_chain):

    print(f"Asking: {question}")
 
    docs = retriever.invoke(question)
    context = "\n\n".join(
    doc.page_content
    for doc in docs
    )


    #LangChain populates chat_prompt with context, question, and chat_history.
    answer = rag_chain.invoke(
       {
        "context": context,
        "question": question,
        "chat_history": chat_history
        }
    )
 #   messages = chat_prompt.format_messages(
  #  context=context,
  #  question=question,
  #  chat_history=chat_history
#)

    #llm=get_llm(application_config)
    #response = llm.invoke(messages) 
       
    return answer

def start_chat(application_config):

    print("AI Knowledge Assistant")
    print("Enter question and type 'exit' to quit:")
    chat_history = []

    embedding_model = get_embedding_model()
    print("Getting retriever.")

    retriever = get_retriever(
        application_config,
        embedding_model
    )

    llm=get_llm(application_config)
    rag_chain = (
        chat_prompt
        | llm
        | StrOutputParser()
    )
    while True:
        
        question=input("You: ")
        if question == "exit":
            return
        answer=ask_question(application_config,retriever,question,chat_history,rag_chain)
        print(f"Answer is:{answer}")
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=answer))




#This method can be used to check top#k chunks retrieved
def invoke_retriever_to_get_context(application_config,question):

    print("Started Retriever.")
    embedding_model = get_embedding_model()
    print("Getting retriever.")

    retriever = get_retriever(
        application_config,
        embedding_model
    )
    #question="What is Test fixtures in playwright?"
    docs = retriever.invoke(
        question
    )

    print("Number of documents retrieved:", len(docs))
    print("Retrieved docs:")
    print("*******************************************")
    for i, doc in enumerate(docs):

        print("=" * 80)
        print(f"Document {i + 1}")

        print("\nMetadata:")
        print(doc.metadata)

        print("\nContent:")
        print(doc.page_content[:500])
    return docs


def invoke_retriever_to_get_context_pagecontent_list(application_config,question):

    print("Started Retriever.")
    embedding_model = get_embedding_model()
    print("Getting retriever.")

    retriever = get_retriever(
        application_config,
        embedding_model
    )
    #question="What is Test fixtures in playwright?"
    docs = retriever.invoke(
        question
    )

    print("Number of documents retrieved:", len(docs))
    print("Retrieved docs:")
    print("*******************************************")
    for i, doc in enumerate(docs):

        print("=" * 80)
        print(f"Document {i + 1}")

        print("\nMetadata:")
        print(doc.metadata)

        print("\nContent:")
        print(doc.page_content[:500])
  # For DeepEval
    retrieval_context = [
        doc.page_content
        for doc in docs
    ]

    return retrieval_context