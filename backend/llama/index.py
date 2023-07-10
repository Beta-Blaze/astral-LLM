from typing import Optional, List, Mapping, Any

from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    LangchainEmbedding,
    ListIndex, VectorStoreIndex, StorageContext, load_index_from_storage
)
from llama_index.llms import CustomLLM, CompletionResponse, LLMMetadata, CompletionResponseGen

from chat_bot import ChatBot, ChatBotSettings

# set context window size
context_window = 2048
# set number of output tokens
num_output = 256

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


# define our LLM
llm = OurLLM()

service_context = ServiceContext.from_defaults(
    llm=llm,
    context_window=context_window,
    num_output=num_output
)

# Load the your data
# documents = SimpleDirectoryReader(r"E:\Develop\OpenBuddy\test").load_data()
# index = VectorStoreIndex.from_documents(documents)
# index.set_index_id("testindex")
# index.storage_context.persist(r"E:\Develop\OpenBuddy\storage")


# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir=r"E:\Develop\OpenBuddy\storage")
# load index
index = load_index_from_storage(storage_context, index_id="testindex")

# Query and print response
query_engine = index.as_query_engine()
response = query_engine.query("Какое последнее событие наполеоновских войн?")
print(response)
