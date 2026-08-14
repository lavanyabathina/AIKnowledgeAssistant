from deepeval import evaluate
from deepeval.test_case import Turn , ConversationalTestCase 
from deepeval.metrics import RoleAdherenceMetric
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


question1="What is inheritance in Java and how is it declared?"
actual_output1=session.ask(question1)
print("Actual output1 is:" ,actual_output1 )
print("*****************************************************")
question2="How do I instantiate a subclass object in Java?"
actual_output2=session.ask(question2)
print("Actual output2 is:" ,actual_output2 )
print("*****************************************************")

question3="How do I create a generator function in Python?"
actual_output3=session.ask(question3)

print("Actual output3 is:" ,actual_output3 )
print("*****************************************************")

chatbot_role = """
You are an AI Knowledge Assistant.

Your job is to answer the user's current question using ONLY
the retrieved context.

Rules:
1. The retrieved context is the ONLY source of factual information.
2. Conversation history can be used only to understand references
   such as "it", "they", "this", or "that".
3. Never use your own general knowledge to answer the question.
4. Never add information that is not supported by the retrieved context.
5. If the answer is not present in the retrieved context, say:
   "The information is not available in the provided documentation."
6. Answer the user's question directly.
7. Do not include unrelated advanced topics.
8. If the question is simple, give a simple explanation.
9. Do not mention APIs or implementation details unless asked.
"""


role_adherence_test= ConversationalTestCase(
 chatbot_role=chatbot_role,
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
metric = RoleAdherenceMetric(threshold=0.5 , model=modelObj)

evaluate(test_cases=[role_adherence_test],metrics=[metric])