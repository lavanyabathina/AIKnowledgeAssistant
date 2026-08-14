from deepeval import evaluate
from deepeval.test_case import Turn , ConversationalTestCase 
from deepeval.metrics import TurnFaithfulnessMetric
from services.chat_session import *
from langchain_groq import ChatGroq
from evaluation.groq_judge import *
from deepeval.models import AnthropicModel

#Requirements to invoke chat llm
load_dotenv()
application_config = load_config('config/application_config.yaml');
session=ChatSession(application_config)

judge_model_provider=application_config["deepeval_judgellm"]["provider"]
judge_model=application_config["deepeval_judgellm"]["model"]

modelObj=""

if judge_model_provider == "groq":
    #model=GroqJudge("llama-3.1-8b-instant")
    modelObj=GroqJudge(judge_model)
elif judge_model_provider == "claude":
    modelObj = AnthropicModel(
    model="claude-sonnet-4-5",
    temperature=0
    )
else:
    print(f"{judge_model} is not yet supported as judge model in this application")


question1="What are common operations supported by Java's String class?"
retrieval_context1= invoke_retriever_to_get_context_pagecontent_list(application_config,question1)
#Here retrieval_context is a list
actual_output1=session.ask(question1)
print("Actual output1 is:" ,actual_output1 )
print("*****************************************************")
question2="What are the differences between String and StringBuffer in Java?"
retrieval_context2= invoke_retriever_to_get_context_pagecontent_list(application_config,question2)
actual_output2=session.ask(question2)
print("Actual output2 is:" ,actual_output2 )
print("*****************************************************")

question3="How do I create and populate a Java HashMap with key-value pairs?"
retrieval_context3= invoke_retriever_to_get_context_pagecontent_list(application_config,question3)

actual_output3=session.ask(question3)

print("Actual output3 is:" ,actual_output3 )
print("*****************************************************")

turn_faithfulness_test= ConversationalTestCase(
 turns=[
 Turn(
    role="user",
    content=question1,
    retrieval_context=retrieval_context1
 ),
 Turn(
    role="assistant",
    content=actual_output1,
    retrieval_context=retrieval_context1
 ),
 Turn(
    role="user",
    content=question2,
    retrieval_context=retrieval_context2
 ),
 Turn(
    role="assistant",
    content=actual_output2,
   retrieval_context=retrieval_context2
 ),
 Turn(
    role="user",
    content=question3,
    retrieval_context=retrieval_context3

 ),
 Turn(
    role="assistant",
    content=actual_output3,
    retrieval_context=retrieval_context3
 )
 ]
)
metric = TurnFaithfulnessMetric(threshold=0.5 , model=modelObj)

evaluate(test_cases=[turn_faithfulness_test],metrics=[metric])