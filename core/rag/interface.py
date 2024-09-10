from abc import ABC, abstractmethod
from langchain_core.prompts import PromptTemplate


class IRetrieval(ABC):
    @abstractmethod
    async def retrieve(self, query: str):
        raise NotImplementedError
    

class IGenerator(ABC):
    @abstractmethod
    async def generate(self, question: str, prompt: PromptTemplate):
        raise NotImplementedError