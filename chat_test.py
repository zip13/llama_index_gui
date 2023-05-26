import os
import time
import sysconfig
from modules import chat_options
from modules.chat_options import cmd_opts
from modules.chat_ui import create_ui,load_index
from env import ini_env
# patch PATH for cpm_kernels libcudart lookup
import sys
import os
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))



ini_env()

# 导入必要的库和模块
from llama_index import ServiceContext, LLMPredictor, PromptHelper, StorageContext, load_index_from_storage
from langchain import OpenAI
from modules.chat_options import cmd_opts
from modules.context import Context

from llama_index.data_structs.node import NodeWithScore
from llama_index.response.schema import Response
from llama_index.utils import truncate_text
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, StorageContext, load_index_from_storage
from pathlib import Path
import os



# 初始化LLM预测器（这里使用gpt-3.5-turbo模型）
llm_predictor = LLMPredictor(llm=OpenAI(temperature=cmd_opts.temperature, model_name=cmd_opts.model_name))

# 构建服务上下文
service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor,
            prompt_helper=PromptHelper(max_input_size=cmd_opts.max_input_size,
            max_chunk_overlap=cmd_opts.max_chunk_overlap,
            num_output=cmd_opts.num_output),
            chunk_size_limit=cmd_opts.chunk_size_limit
            )

# 构建存储上下文
storage_context = StorageContext.from_defaults(persist_dir=cmd_opts.persist_dir)

# 加载索引
index = load_index_from_storage(storage_context, service_context=service_context)

index_set = {}
index_set[0]=index

from llama_index import GPTListIndex, LLMPredictor, ServiceContext, load_graph_from_storage
from langchain import OpenAI
from llama_index.indices.composability import ComposableGraph
# describe each index to help traversal of composed graph
index_summaries = [f"丰迈公司产品介绍"]

# define an LLMPredictor set number of output tokens
llm_predictor = LLMPredictor(llm=OpenAI(temperature=cmd_opts.temperature, model_name=cmd_opts.model_name))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
storage_context = StorageContext.from_defaults()

# define a list index over the vector indices
# allows us to synthesize information across each index
graph = ComposableGraph.from_indices(
    GPTListIndex,
    [index_set[0] ], 
    index_summaries=index_summaries,
    service_context=service_context,
    storage_context = storage_context,
)
root_id = graph.root_id

# [optional] save to disk
storage_context.persist(persist_dir=f'./storage/root')

# [optional] load from disk, so you don't need to build graph from scratch
graph = load_graph_from_storage(
    root_id=root_id, 
    service_context=service_context,
    storage_context=storage_context,
)

from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig
# define a decompose transform
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform
decompose_transform = DecomposeQueryTransform(
    llm_predictor, verbose=True
)

# define custom retrievers
from llama_index.query_engine.transform_query_engine import TransformQueryEngine

custom_query_engines = {}
for index in index_set.values():
    query_engine = index.as_query_engine()
    query_engine = TransformQueryEngine(
        query_engine,
        query_transform=decompose_transform,
        transform_extra_info={'index_summary': index.index_struct.summary},
    )
    custom_query_engines[index.index_id] = query_engine
custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
    response_mode='tree_summarize',
    verbose=True,
)

# tool config
graph_config = IndexToolConfig(
    query_engine=custom_query_engines[graph.root_id],
    name=f"Graph Index",
    description="useful for when you want to answer queries that require analyzing multiple SEC 10-K documents for 丰迈.",
    tool_kwargs={"return_direct": True}
)

# define toolkit
index_configs = []

query_engine = index_set[0].as_query_engine(
    similarity_top_k=3,
)
tool_config = IndexToolConfig(
    query_engine=query_engine, 
    name=f"Vector Index 0",
    description=f"useful for when you want to answer queries about the  SEC 10-K for Uber",
    tool_kwargs={"return_direct": True}
)
index_configs.append(tool_config)
toolkit = LlamaToolkit(
    index_configs=index_configs 
)

memory = ConversationBufferMemory(memory_key="chat_history")
llm=OpenAI(temperature=0)
agent_chain = create_llama_chat_agent(
    toolkit,
    llm,
    memory=memory,
    verbose=True
)

while True:
    text_input = input("User: ")
    response = query_engine.query(text_input)
    print(f'Agent0: {response}')
    response = agent_chain.run(input=text_input)
    print(f'Agent: {response}')
