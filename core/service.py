from abc import ABC, abstractmethod
from core.util import clean_answer
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


class IRAG(ABC):
    @abstractmethod
    async def generate(self, question: str, prompt: ChatPromptTemplate):
        raise NotImplementedError


class RAG:
    def __init__(self, retrieval, generator):
        self.retrieval = retrieval
        self.generator = generator

    async def generate(self, question: str, prompt: ChatPromptTemplate):
        document_chain = create_stuff_documents_chain(self.generator, prompt)
        retrieval_chain = create_retrieval_chain(self.retrieval, document_chain)

        answer = retrieval_chain.invoke({"input": question})
        
        cleaned_answer = clean_answer(answer["answer"])
        return cleaned_answer
        