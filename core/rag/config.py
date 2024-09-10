
from dataclasses import dataclass
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


@dataclass
class ColBERTConfig:
    experiment_path: str = "/app/data/experiments/experiments/msmarco"
    index_name: str = "heyhi"
    checkpoint: str = "ghanahmada/biology-mcolbert"


@dataclass
class LlaMa38BInstructConfig:
    model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    hf_api_token: str = "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"
    max_new_tokens: int = 768
    top_k: int = 10
    top_p: float = 0.95
    typical_p: float = 0.95
    temperature: float = 0.01
    repetition_penalty: float = 1.03
    streaming: bool = False
    return_full_text: bool = False


@dataclass
class BasePrompt:
    prompt: PromptTemplate= PromptTemplate.from_template(
      """
      Jawab pertanyaan berikut sebagai guru sesuai dengan bahasa yang digunakan dalam pertanyaan.

      Question: {input}

      Note: Answer in the same language as the question.
      """
        )


@dataclass
class RAGPrompt:
    prompt: ChatPromptTemplate= ChatPromptTemplate.from_template(
      """
      Jawab pertanyaan berikut sebagai guru sesuai dengan bahasa yang digunakan dalam pertanyaan. Jangan jawab
      bila pertanyaan berkaitan dengan isu kekerasan, sex, LGBT, dan hal buruk lainnya. Gunakan tone ramah dan friendly

      <context>
      {context}
      </context>
      Apabila pertanyaan tidak sesuai dengan konteks yang dibahas, maka jawab saja pertanyaan dengan pengetahuan yang ada.
      Question: {input}

      Note: Answer in the same language as the question.
      """
    )
