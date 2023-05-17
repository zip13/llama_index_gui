from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper

from langchain import OpenAI
import sys
import os
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

#openai key
os.environ["OPENAI_API_KEY"] = 'your openai key'
#代理
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

def construct_index(directory_path):

    max_input_size = 4096

    num_outputs = 512

    max_chunk_overlap = 20

    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.3, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
   
    #index.save_to_disk('index.json')
    index.storage_context.persist(persist_dir='./storage')
    return index



construct_index("docs")
