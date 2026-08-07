# test_deepeval_anthropic.py

from deepeval.models import AnthropicModel

model = AnthropicModel(
    model="claude-sonnet-4-6",
    temperature=0
)

response = model.generate(
    "Explain RAG in two sentences."
)

print(response)