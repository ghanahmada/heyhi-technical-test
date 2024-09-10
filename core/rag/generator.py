from core.rag.interface import IGenerator
from core.rag.config import LlaMa38BInstructConfig
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint


class LlaMa38BInstructGenerator(IGenerator):
    def __init__(self, config: LlaMa38BInstructConfig):
        self.config = config
        self._init_llm()

    def _init_llm(self):
        self.llm = HuggingFaceEndpoint(
                repo_id=self.config.model_name,
                huggingfacehub_api_token=self.config.hf_api_token,
                max_new_tokens=self.config.max_new_tokens,
                top_k=self.config.top_k,
                top_p=self.config.top_p,
                typical_p=self.config.typical_p,
                temperature=self.config.temperature,
                repetition_penalty=self.config.repetition_penalty,
                streaming=self.config.streaming,
                return_full_text=self.config.return_full_text,
            )

    async def generate(self, question: str, prompt: PromptTemplate):
        llm_chain = prompt | self.llm
        response = llm_chain.invoke({"input": question})
        return response

        
