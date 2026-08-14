from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric
from services.chat_session import *
from langchain_groq import ChatGroq
from evaluation.groq_judge import *
from deepeval.models import AnthropicModel
from pipelines.chat_pipeline import *

print("Failthfulmess metric Testing")
#Requirements to invoke chat llm and retrieve context to test
load_dotenv()
application_config = load_config('config/application_config.yaml');
judge_model_provider=application_config["deepeval_judgellm"]["provider"]
judge_model=application_config["deepeval_judgellm"]["model"]

modelObj=""

if judge_model_provider == "groq":
    #model=GroqJudge("llama-3.1-8b-instant")
    modelObj=GroqJudge(judge_model)
elif judge_model_provider == "claude":
    modelObj = AnthropicModel(
    model=judge_model,
    temperature=0
    )
else:
    print(f"{judge_model} is not yet supported as judge model in this application")

session=ChatSession(application_config)
metric = FaithfulnessMetric(
    threshold=0.6,
    model=modelObj,
    include_reason=True
)
question1="What is the syntax to create a list in Python?"
actual_output1=session.ask(question1)
print("Actual output1 is:" ,actual_output1 )
print("*****************************************************")
retrieval_context1= invoke_retriever_to_get_context_pagecontent_list(application_config,question1)
print("retrieval context1 is:" , retrieval_context1 )
print("*****************************************************")

question2="What is a class in Python and how do I define one?"
actual_output2=session.ask(question2)
print("Actual output2 is:" ,actual_output2 )
print("*****************************************************")
retrieval_context2= invoke_retriever_to_get_context_pagecontent_list(application_config,question2)
print("retrieval context2 is:" , retrieval_context2 )
print("*****************************************************")


test_case1=LLMTestCase(
    input=question1,
    actual_output=actual_output1,
    retrieval_context=retrieval_context1

)

test_case2=LLMTestCase(
    input=question2,
    actual_output=actual_output2,
    retrieval_context=retrieval_context2
)

evaluate(test_cases=[test_case1,test_case2] , metrics=[metric])