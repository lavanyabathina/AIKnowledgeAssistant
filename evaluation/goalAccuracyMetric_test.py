from deepeval import evaluate
from deepeval.test_case import Turn , ConversationalTestCase 
from deepeval.metrics import GoalAccuracyMetric
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


question1="What is a Java interface and when should I use it?"
actual_output1=session.ask(question1)
print("Actual output1 is:" ,actual_output1 )
print("*****************************************************")
question2="How do I create an instance of a Java class using a constructor?"
actual_output2=session.ask(question2)
print("Actual output2 is:" ,actual_output2 )
print("*****************************************************")

question3="In Python, how do I define a function that accepts variable keyword arguments (kwargs)?"
actual_output3=session.ask(question3)

print("Actual output3 is:" ,actual_output3 )
print("*****************************************************")

goalAccuracy_test= ConversationalTestCase(
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
metric = GoalAccuracyMetric(threshold=0.5 , model=modelObj)

evaluate(test_cases=[goalAccuracy_test],metrics=[metric])