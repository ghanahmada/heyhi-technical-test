import os
import gdown
import zipfile
import logging
from typing import Any
from langchain_core.retrievers import BaseRetriever
from core.rag.retriever import ColBERTLangChainRetriever


def as_langchain_retriever(model, **kwargs: Any) -> BaseRetriever:
    return ColBERTLangChainRetriever(model=model, kwargs=kwargs)

def clean_answer(answer: str) -> str:
    truncted_idx = answer.find(":")
    if truncted_idx < 15:
        answer = answer[truncted_idx + 1:]
    return answer.replace("<|eot_id|>", "").strip()

def check_dir(dir_name: str) -> bool:
    return os.path.isdir(dir_name)

def download_data(url, filename, dir_name: str = "experiments") -> None:
    if not check_dir(dir_name):
        os.mkdir(dir_name)
    os.chdir(dir_name)

    logging.info("Downloading data....")
    gdown.download(url, quiet=False)
    print(f"dowloading: {os.getcwd()}", flush=True)
    logging.info("Extracting zip file....")
    with zipfile.ZipFile(f"{filename}.zip", 'r') as zip_ref:
        zip_ref.extractall(filename)
    os.remove(f"{filename}.zip")
    os.chdir("..")