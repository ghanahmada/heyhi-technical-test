from typing import Any, List
from core.rag.interface import IRetrieval
from core.rag.config import ColBERTConfig

import colbert
from colbert import Searcher
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Collection
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun


class ColBERTLangChainRetriever(BaseRetriever):
    model: Any
    kwargs: dict = {}

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun,
    ) -> List[Document]:
        """Get documents relevant to a query using the ColBERT searcher."""

        results = self.model.search(query, **self.kwargs)

        documents = [
            Document(
                page_content=self.model.collection[passage_id],
                metadata={"passage_id": passage_id, "rank": passage_rank, "score": passage_score}
            )
            for passage_id, passage_rank, passage_score in zip(*results)
        ]

        return documents


class ColBERTRetriever(IRetrieval):
    def __init__(self, config: ColBERTConfig):
        self.config = config

        self._init_searcher()

    def _init_searcher(self):
        with Run().context(RunConfig(experiment=self.config.experiment_path)):
            self.searcher = Searcher(index=self.config.index_name, checkpoint=self.config.checkpoint)

        self.searcher.search("init...", k=1)

    async def retrieve(self, query: str, k: int=1):
        results = self.searcher.search(query, k=k)
        passage_id, passage_rank, passage_score = zip(*results)
        retrieved_passage = await Collection().get_passages(passage_id)
        return retrieved_passage

    

            