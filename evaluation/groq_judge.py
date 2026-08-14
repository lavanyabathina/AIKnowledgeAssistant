
#DeepEval 4.1.5's AnswerRelevancyMetric does not accept LangChain ChatGroq directly. 
#It should be one of these types
#DeepEvalBaseLLM
#GPTModel
#AzureOpenAIModel
#LiteLLMModel
#OllamaModel
#LocalModel
from deepeval.models import DeepEvalBaseLLM
from langchain_groq import ChatGroq
class GroqJudge(DeepEvalBaseLLM):
    def __init__(self,model_name):
        self.model_name=model_name
        self.model = ChatGroq(
            model=model_name,
            temperature=0
        )
    def load_model(self):
        return self.model


    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response.content
    
    async def a_generate(self, prompt: str) -> str:
        response = await self.model.ainvoke(prompt)
        return response.content

    def get_model_name(self):
        return self.model_name