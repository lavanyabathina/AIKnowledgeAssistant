from deepeval import evaluate
from deepeval.test_case import Turn , ConversationalTestCase 
from deepeval.metrics import KnowledgeRetentionMetric
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
    model=judge_model,
    temperature=0
    )
else:
    print(f"{judge_model} is not yet supported as judge model in this application")


question1="Explain Java access modifiers (public, protected, private) and their visibility rules."
actual_output1=session.ask(question1)
print("Actual output1 is:" ,actual_output1 )
print("*****************************************************")
question2="Show how to instantiate an object in Java and call one of its methods."
actual_output2=session.ask(question2)
print("Actual output2 is:" ,actual_output2 )
print("*****************************************************")

question3="How can I document a Python function using a docstring?"
actual_output3=session.ask(question3)

print("Actual output3 is:" ,actual_output3 )
print("*****************************************************")

knowledgeRetention_test= ConversationalTestCase(
 turns=[
 Turn(
    role="user",
    content=question1
 ),
 Turn(
    role="assistant",
    content=actual_output1
 ),
 Turn(
    role="user",
    content=question2
 ),
 Turn(
    role="assistant",
    content=actual_output2
 ),
 Turn(
    role="user",
    content=question3
 ),
 Turn(
    role="assistant",
    content=actual_output3
 )
 ]
)
metric = KnowledgeRetentionMetric(threshold=0.5 , model=modelObj)

evaluate(test_cases=[knowledgeRetention_test],metrics=[metric])