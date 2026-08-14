from deepeval import evaluate
from deepeval.test_case import Turn , ConversationalTestCase , LLMTestCase
from deepeval.metrics import ContextualPrecisionMetric , ContextualRecallMetric
from services.chat_session import *
from langchain_groq import ChatGroq
from evaluation.groq_judge import *
from deepeval.models import AnthropicModel
import json
from pathlib import Path

#Requirements to invoke chat llm
load_dotenv()
application_config = load_config('config/application_config.yaml');
judge_model_provider=application_config["deepeval_judgellm"]["provider"]
judge_model=application_config["deepeval_judgellm"]["model"]
dataset_path = Path(__file__).parent / "golden_dataset.json"



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

metric1 = ContextualPrecisionMetric(
    threshold=0.6,
    model=model,
    include_reason=True
)
metric2 = ContextualRecallMetric(
    threshold=0.6,
    model=model,
    include_reason=True
)
with open(dataset_path) as file:
    entries=json.load(file)
test_cases=[]
for entry in entries:
    question = entry["question"]
    expected_output= entry["expected_output"]
    actual_output=session.ask(question)
    retrieval_context= invoke_retriever_to_get_context_pagecontent_list(application_config,question)

    test_case=LLMTestCase(
        input=question,
        actual_output=actual_output,
        expected_output=expected_output,
        retrieval_context=retrieval_context
    )
    test_cases.append(test_case)


evaluate(test_cases=test_cases, metrics=[metric1,metric2])

