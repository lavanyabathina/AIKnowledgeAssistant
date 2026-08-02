from loaders.load_config import *
from pipelines.dataset_pipeline import *
from pipelines.vector_pipeline import *
from pipelines.chat_pipeline import *
from dotenv import load_dotenv

import asyncio
import time

async def main():
    print ("Loading .env file")
    load_dotenv()
    print("Loading config files.")
    application_config = load_config('config/application_config.yaml');
    dataset_config = load_config('config/dataset_config.yaml');

    if application_config["application"]["dataset_generation"]["enabled"]:
        await generate_dataset(dataset_config)
    
    if application_config["application"]["rebuild_vector_db"]["enabled"]:
        vectorDBPath = application_config["vector_db"]["path"]
        delete_chromadb(vectorDBPath)
    
    if application_config["application"]["vector_indexing"]["enabled"]:
        build_vector_db(dataset_config, application_config)

    if application_config["application"]["chat"]["enabled"]:
        #start_chart method can be used to get top-k searches by invoking retriver 
        print("Starting Chat")
        start_chat(application_config)
        #question1="what is test fixture in playwright?"
        #print(f"Asking question:{question1}")
        #answer1=ask_question(application_config , question1)
        #print(f"Answer is: {answer1[0]["text"]}" )

        #question2="what is implicit wait in selenium?"
        #print(f"Asking question:{question2}")
        #answer2=ask_question(application_config , question2)
        #print(f"Answer is: {answer2[0]["text"]}" )

        #question3="what is async in playwright?"
        #print(f"Asking question:{question3}")
        #answer3=ask_question(application_config , question3)
        #print(f"Answer is: {answer3[0]["text"]}" )

        #question4="what is driver in selenium?"
        #print(f"Asking question:{question4}")
        #answer4=ask_question(application_config , question4)
        #print(f"Answer is: {answer4[0]["text"]}" )
   
   
   
    #Code to delete one collection
    #collections= list_collections("./vectorstore/chroma_db")
    #print("Collections Before delete:" , collections)

    #delete_collection("./vectorstore/chroma_db", "knowledge_base")
    
    #collections= list_collections("./vectorstore/chroma_db")
    #print("Collections After delete:" , collections)
   
   

if __name__ == "__main__":
        asyncio.run(main())
 