from deepeval import evaluate
from deepeval.test_case import Turn , ConversationalTestCase , LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from services.chat_session import *
from langchain_groq import ChatGroq
from evaluation.groq_judge import *
from deepeval.models import AnthropicModel

#Requirements to invoke chat llm
load_dotenv()
application_config = load_config('config/application_config.yaml');
judge_model_provider=application_config["deepeval_judgellm"]["provider"]
judge_model=application_config["deepeval_judgellm"]["model"]



print("Answer Relevancy Metric Testcase")

if judge_model_provider == "groq":
    #model=GroqJudge("llama-3.1-8b-instant")
    model=GroqJudge(judge_model)
elif judge_model_provider == "claude":
    model = AnthropicModel(
    model=judge_model,
    temperature=0
    )
else:
    print(f"{judge_model} is not yet supported as judge model in this application")
session=ChatSession(application_config)

metric = AnswerRelevancyMetric(
    threshold=0.6,
    model=model,
    include_reason=True
)

question1="What is class in Java?"
actual_output1=session.ask(question1)
print("Actual output1 is:" ,actual_output1 )
print('******************************************')
question2="What is the difference between String and String Buffer in Java?"
actual_output2=session.ask(question2)
print("Actual output2 is:" ,actual_output2 )

print('******************************************')
question3="Which are different loops available in Python?"
actual_output3=session.ask(question3)




print("Actual output3 is:" ,actual_output3 )

print('******************************************')
test_case1=LLMTestCase(

    input=question1,
    actual_output=actual_output1

)
test_case2=LLMTestCase(

    input=question2,
    actual_output=actual_output2

)
test_case3=LLMTestCase(

    input=question3,
    actual_output=actual_output3

)
evaluate(test_cases=[test_case1,test_case2,test_case3],metrics=[metric])


