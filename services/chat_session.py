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

        self.llm=get_llm(app_config)
        self.rag_chain = (
        chat_prompt
        | self.llm
        | StrOutputParser()
        )

    def ask(self,question:str):
        
        answer=ask_question(self.app_config,self.retriever,question,self.chat_history,self.rag_chain,self.llm)
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer))
        return answer


if __name__ == "__main__":
    print("In Chat_session")
    load_dotenv()

    application_config = load_config('config/application_config.yaml');

    session = ChatSession(application_config)
    question1="What is Class in java?"
    print("Question is:" , question1)
    answer1 = session.ask(question1)
    print("Answer is:",answer1)
    question2="How do I create an object from it?"
    print("Question is:" , question2)
    answer2 = session.ask(question2)
    print("Answer is:",answer2)
    question3="What is the difference between StringBuffer and String?"
    answer3 = session.ask(question3)
    print("Answer is:",answer3)
  

   
