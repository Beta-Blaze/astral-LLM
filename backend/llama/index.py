import os

import numpy as np
import pandas as pd
from openai.embeddings_utils import cosine_similarity

from chat_bot import ChatBot, ChatBotSettings
from text2vec import SentenceModel


class SimpleDocumentStore:
    def __init__(self):
        self.documents = []

    def add_documents(self, documents):
        self.documents.append(documents)

    def get_documents(self):
        return self.documents

    def __len__(self):
        return len(self.documents)

    def __getitem__(self, index):
        return self.documents[index]

    def __iter__(self):
        return iter(self.documents)

    def is_empty(self):
        return len(self.documents) == 0


class EmbeddingSettings:
    def __init__(self, chunk_size: int = 300, output_size: int = 3,
                 model_name: str = "shibing624/text2vec-base-multilingual",
                 save_path: str = "./index"):
        self.chunk_size = chunk_size
        self.output_size = output_size
        self.save_path = save_path
        self.model_name = model_name


class EmbeddingIndex:
    def __init__(self, settings: EmbeddingSettings, llm: ChatBot):
        self.settings: EmbeddingSettings = settings
        self.llm: ChatBot = llm
        self.index: pd.DataFrame = pd.DataFrame()
        self.docstore: SimpleDocumentStore = SimpleDocumentStore()
        self.query_engine: ChatBot.chat = llm.chat
        self.embed_model: SentenceModel = SentenceModel(self.settings.model_name)

    def add_documents(self, documents_path: str):
        if not os.path.exists(documents_path):
            return
        with open(documents_path, "r", encoding="utf-8") as f:
            document = f.read()
            self.docstore.add_documents(document)

    def read_index(self):
        if os.path.exists(self.settings.save_path + "/embedded.csv"):
            self.index = pd.read_csv(self.settings.save_path + "/embedded.csv")
            self.index['embedded'] = self.index.embedded.apply(eval).apply(np.array)
        else:
            self.create_index()

    def create_index(self):
        if self.docstore.is_empty():
            return

        self.index = pd.DataFrame()

        temp = []
        for text in self.docstore:
            temp.extend([text[i:self.settings.chunk_size + i]
                         for i in range(0, len(text), self.settings.chunk_size)])

        self.index["combined"] = temp

        self.index["embedded"] = self.index.combined.apply(
            lambda x: self.embed_model.encode(x).tolist())

        self.index.to_csv(self.settings.save_path + "/embedded.csv", index=False)

    def search(self, query: str) -> str:
        query_embedding = self.embed_model.encode(query)

        self.index['similarities'] = self.index.embedded.apply(
            lambda x: cosine_similarity(x, query_embedding))

        res = self.index.sort_values(by='similarities', ascending=False) \
            .head(self.settings.output_size)

        string = ""

        for i, row in res.iterrows():
            string += row.combined + "\n"

        return string

    def query(self, query: str):
        data = self.search(query)

        # print(data)

        print("Answer:")

        question = f"""Context information is below.
        ----- {data} -----
        Given the context information and not prior knowledge, answer the question in Russian: {query}
        
        """

        for response in self.query_engine(question):
            print(response, end="")


if __name__ == "__main__":
    e_settings = EmbeddingSettings()
    s_settings = ChatBotSettings(
        req_url='http://localhost:8000/v1/chat/completions',
        authorization='Bearer token',
        organization='LLC BetaBlaze&AlanShan',
        model=r'E:\git\astral-LLM\backend\llama\models\ru-openllama-7b-v5-q5_K.bin',
        max_tokens=3488,
        temperature=0.6,
    )

    llm = ChatBot(s_settings)
    index = EmbeddingIndex(e_settings, llm)
    index.add_documents(r"E:\git\astral-LLM\backend\llama\index\test.txt")
    index.create_index()
    index.read_index()
    index.query("Что означает красный статус контрагента?")
