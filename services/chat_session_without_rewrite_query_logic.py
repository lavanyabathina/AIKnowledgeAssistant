from retrieval.retriever import get_retriever
from processors.embedding_generator import *
from llm.llm_factory import *
from chat.chat_prompt import chat_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from pipelines.chat_pipeline import *
from loaders.load_config import *
from dotenv import load_dotenv



class ChatSession :

    def __init__(self,app_config):
        self.chat_history = []
        self.app_config = app_config
    
    
        embedding_model = get_embedding_model()
        print("Getting retriever.")
        self.retriever = get_retriever(
        app_config,
        embedding_model
        )

        llm=get_llm(app_config)
        self.rag_chain = (
        chat_prompt
        | llm
        | StrOutputParser()
        )

    def ask(self,question:str):
        
        answer=ask_question(self.app_config,self.retriever,question,self.chat_history,self.rag_chain)
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer))
        return answer


if __name__ == "__main__":
    print("In Chat_session")
    load_dotenv()

    application_config = load_config('config/application_config.yaml');

    session = ChatSession(application_config)

    answer1 = session.ask("What is Class in java?")
    print("Answer is:",answer1)
    answer2 = session.ask("Give me an example.")
    print("Answer is:",answer2)

    answer3 = session.ask("What is the difference between StringBuffer and String?")
    print("Answer is:",answer3)
    print("*********************************************************")
    print("Chat History is:" , session.chat_history)

   
