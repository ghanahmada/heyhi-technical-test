import os
from core.rag.retriever import ColBERTRetriever, ColBERTLangChainRetriever
from core.rag.generator import LlaMa38BInstructGenerator
from core.rag.config import ColBERTConfig, LlaMa38BInstructConfig
from core.service import RAG
from core.util import download_data, as_langchain_retriever
from django.conf import settings


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        key = (cls, args, frozenset(kwargs.items()))
        if key not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[key] = instance
        return cls._instances[key]

class QAEngine(metaclass=SingletonMeta):
    def __init__(self):
        self.retriever = as_langchain_retriever(ColBERTRetriever(ColBERTConfig).searcher, k=1)
        self.generator = LlaMa38BInstructGenerator(LlaMa38BInstructConfig)
        self.rag = RAG(self.retriever, self.generator.llm)


def initialize_qa_engines():
    global engine

    print("Initializing QAEngine instances...")
    engine = QAEngine()
    print("QAEngine instances have been initialized.")


def setup_index():
    print("Downloading index...")
    print(os.getcwd(), flush=True)
    download_data(url="https://drive.google.com/uc?&id=1n-KkrUpfVncfP_vbsyYMgCzGhclVTu8i",
              filename="experiments",
              dir_name="data")
    print(os.getcwd(), flush=True)
    print("Index has been downloaded.")