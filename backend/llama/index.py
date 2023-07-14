from typing import Optional, List, Mapping, Any

from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    LangchainEmbedding,
    VectorStoreIndex,
    ListIndex, VectorStoreIndex, StorageContext, load_index_from_storage, LLMPredictor, PromptHelper
)
from llama_index.llms import CustomLLM, CompletionResponse, LLMMetadata, CompletionResponseGen
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore import SimpleDocumentStore

from chat_bot import ChatBot, ChatBotSettings

# set context window size
context_window = 2048

# store the pipeline/model outisde of the LLM class to avoid memory issues
model_name = r"E:\Develop\OpenBuddy\models\llama-13b-v5-q5_K.bin"


class OurLLM(CustomLLM):
    def __init__(self):
        super().__init__()
        settings = ChatBotSettings(
            req_url='http://localhost:8000/v1/chat/completions',
            authorization='Bearer token',
            organization='LLC BetaBlaze&AlanShan',
            model=r'E:\Develop\OpenBuddy\models\llama-13b-v5-q5_K.bin',
            max_tokens=3000,
            temperature=0.6,
            stream=False
        )
        self.bot = ChatBot(settings)

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=context_window, num_output=num_output
        )

    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        text = self.bot.perform_index_request_with_openAI(prompt)
        print("Complete called")
        return CompletionResponse(text=text)

    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        raise NotImplementedError()

    def _identifying_params(self):
        return {"name_of_model": "dolly-v2-3b"}

    def _llm_type(self):
        return "custom"

    def _call(self, prompt, stop=None):
        text = self.bot.perform_index_request_with_openAI(prompt)
        print("Complete called")
        return text


# define our LLM
llm = OurLLM()

# service_context = ServiceContext.from_defaults(
#     llm=llm,
#     chunk_size=1024
# )

# Load the your data
# documents = SimpleDirectoryReader(r"E:\Develop\OpenBuddy\test").load_data()
# index = VectorStoreIndex.from_documents(documents)
# index.set_index_id("testindex")
# index.storage_context.persist(r"E:\Develop\OpenBuddy\storage")


# # rebuild storage context
# storage_context = StorageContext.from_defaults(persist_dir=r"E:\Develop\OpenBuddy\storage")
# # # load index
# index = load_index_from_storage(storage_context, index_id="testindex", service_context=service_context)
# #
# # # Query and print response
# query_engine = index.as_query_engine(
#     similarity_top_k=3,
#     vector_store_query_mode="default",
#     alpha=None,
#     doc_ids=None,
# )
# response = query_engine.query("ffffffffffffff?")
# print(response)


# reader = SimpleDirectoryReader(r"E:\Develop\OpenBuddy\test")
# documents = reader.load_data()
#
# nodes = SimpleNodeParser().get_nodes_from_documents(documents)
#
# docstore = SimpleDocumentStore()
# docstore.add_documents(nodes)
#
# storage_context = StorageContext.from_defaults(docstore=docstore)
# vector_index = VectorStoreIndex(nodes, storage_context=storage_context,
#                                 service_context=service_context)
#
# query_engine = vector_index.as_query_engine()
# response = query_engine.query("What did the author do after his time at NYC?")
#
# print(response)


max_input_size = 512
num_output = 200
max_chunk_overlap = 0
chunk_size_limit = 100

llm_predictor = LLMPredictor(llm=OurLLM())

embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name='shibing624/text2vec-base-multilingual'))
# prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, embed_model=embed_model)

documents = SimpleDirectoryReader(r'E:\Develop\OpenBuddy\test').load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
index.storage_context.persist(r'E:\Develop\OpenBuddy\storage_12')

# LOAD INDEX FROM STORAGE
# storage_context = StorageContext.from_defaults(persist_dir=r"E:\Develop\OpenBuddy\storage3")
# index = load_index_from_storage(storage_context, service_context=service_context)

query_text = "Что означает красный статус контрагента?"
response = index.as_query_engine(similarity_top_k=3,
                                 vector_store_query_mode="default",
                                 alpha=None,
                                 doc_ids=None).query(query_text)
print(response)
