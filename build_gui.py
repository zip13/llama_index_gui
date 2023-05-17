from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os
import logging
import gradio as gr

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

#openai key
os.environ["OPENAI_API_KEY"] = 'your openai key'
#代理
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"

def construct_index(folder_path,temperature,max_input_size,num_outputs,max_chunk_overlap,chunk_size_limit,folder_output_path):

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=temperature, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(folder_path).load_data()
    index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
   
    index.storage_context.persist(persist_dir=folder_output_path)
    return "保存成功"


def BuildDig():
    
    #设置一个对话窗

    folder_path = gr.inputs.Textbox(label="请输入文档目录",default="./docs")
    temperature_slider = gr.inputs.Slider(minimum=0.1, maximum=1.0, step=0.1, default=0.7, label="温度")
    max_input_size = gr.inputs.Slider(minimum=512, maximum=8192, default=4096, step=512, label="最大输入长度")
    num_outputs = gr.inputs.Slider(minimum=64, maximum=1024, default=512, step=64, label="输出长度")
    max_chunk_overlap = gr.inputs.Slider(minimum=10, maximum=50, default=20, step=5, label="最大分块重叠单词数")
    chunk_size_limit = gr.inputs.Slider(minimum=200, maximum=1000, default=600, step=100, label="分块大小限制")
    folder_output_path = gr.inputs.Textbox(label="请选择文档目录",default="./storage")
    demo = gr.Interface(
        construct_index,
        # 添加state组件
        [folder_path,temperature_slider,max_input_size,num_outputs,max_chunk_overlap,chunk_size_limit,folder_output_path],
        ["text"],
        # 设置没有保存数据的按钮
        allow_flagging="never",
    )
   

   
    return demo



BuildDig().launch(share=True,server_port=8080,server_name="127.0.0.1")