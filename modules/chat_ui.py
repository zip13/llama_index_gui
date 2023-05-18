from llama_index import ServiceContext, LLMPredictor, PromptHelper,StorageContext, load_index_from_storage
from langchain import OpenAI
from modules.chat_options import cmd_opts
from modules.context import Context

from llama_index.data_structs.node import NodeWithScore
from llama_index.response.schema import Response
from llama_index.utils import truncate_text

import gradio as gr
import os



css = "style.css"
script_path = "scripts"
_gradio_template_response_orig = gr.routes.templates.TemplateResponse


index=None

def load_index():
    global index
     # LLM Predictor (gpt-3.5-turbo)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=cmd_opts.temperature, model_name=cmd_opts.model_name
                                            #, streaming=True
                                            ))
    service_context = ServiceContext.from_defaults(
                llm_predictor=llm_predictor,
                prompt_helper=PromptHelper(max_input_size=cmd_opts.max_input_size,
                max_chunk_overlap=cmd_opts.max_chunk_overlap,
                num_output=cmd_opts.num_output),
                chunk_size_limit=cmd_opts.chunk_size_limit
                )
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=cmd_opts.persist_dir)
    # load index
    index = load_index_from_storage(storage_context,service_context=service_context)

def chat(ctx, message, model_type,refFlag):
    global index,first
    if not index:
        raise "index not loaded"
    ctx.limit_round()
  
    query_engine = index.as_query_engine(
        #streaming=True,
        similarity_top_k=cmd_opts.similarity_top_k,
        response_mode=model_type
    )


    response = query_engine.query(message)

    
    print(response)
    refDoc = []  
    for node in response.source_nodes:  
        if node.similarity != None:  
            refDoc.append(pprint_source_node(node)) # 此处我提前将文档路径设为了doc_id，你也可以设在extra_info里
    if(refFlag):
        res = "".join([
            response.response,  
            "\n引用:\n",  
            "\n".join(refDoc)])
    else: 
        res = response.response
    ctx.append(message, res)
    ctx.refresh_last()
    return ctx.rh

# def save(ctx):
#     pyperclip.copy("\n".join([f"User: {q}\nBot: {a}" for q, a in ctx.rh]))


def pprint_source_node(
    source_node, source_length: int = 350, wrap_width: int = 70
) -> None:
    """Display source node for jupyter notebook."""
    source_text_fmt = truncate_text(source_node.node.get_text().strip(), source_length)
    # print(f"Document ID: {source_node.node.doc_id}")
    # print(f"Similarity: {source_node.score}")
    # print(textwrap.fill(f"Text: {source_text_fmt}\n", width=wrap_width))
    return "".join([
        f'(相似度{source_node.similarity}) ',  
        "\nnode id:",
        source_node.doc_id,  
        "\n",
        source_text_fmt]) 

def pprint_response(
    response: Response, source_length: int = 350, wrap_width: int = 70
) -> None:
    """Pretty print response for jupyter notebook."""
    if response.response is None:
        response_text = "None"
    else:
        response_text = response.response.strip()

    response_text = f"Final Response: {response_text}"
    print(textwrap.fill(response_text, width=wrap_width))

    for ind, source_node in enumerate(response.source_nodes):
        print("_" * wrap_width)
        print(f"Source Node {ind + 1}/{len(response.source_nodes)}")
        pprint_source_node(
            source_node, source_length=source_length, wrap_width=wrap_width
        )


def create_ui():
    reload_javascript();
    with gr.Blocks(analytics_enabled=False) as chat_interface:
        _ctx = Context()
        state = gr.State(_ctx)
        with gr.Row():
            with gr.Column(scale=3):
                input=gr.inputs.Textbox(lines=7, label="请输入")
                model_type = gr.inputs.Radio(
                    choices=["tree_summarize", "compact", "simple_summarize", "refine", "generation"],
                    label="选择模型",
                    default="simple_summarize",  # 使用第一个选项作为默认值
                )
                refFlag=gr.inputs.Checkbox( default=True, label="显示引用", optional=False)
                submit = gr.Button("发送", elem_id="c_generate")
        
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(elem_id="c_chatbot", show_label=False).style(height=500)
                savebutton = gr.Button("保存", elem_id="c_save")
        #设置一个对话窗
        submit.click(chat, inputs=[
                state,
                input,
                model_type,
                refFlag
                
            ], outputs=[
                chatbot,
               
            ])
       
    return chat_interface

def reload_javascript():
    scripts_list = [os.path.join(script_path, i) for i in os.listdir(script_path) if i.endswith(".js")]
    javascript = ""
    # with open("script.js", "r", encoding="utf8") as js_file:
    #     javascript = f'<script>{js_file.read()}</script>'

    for path in scripts_list:
        with open(path, "r", encoding="utf8") as js_file:
            javascript += f"\n<script>{js_file.read()}</script>"

    # todo: theme
    # if cmd_opts.theme is not None:
    #     javascript += f"\n<script>set_theme('{cmd_opts.theme}');</script>\n"

    def template_response(*args, **kwargs):
        res = _gradio_template_response_orig(*args, **kwargs)
        res.body = res.body.replace(
            b'</head>', f'{javascript}</head>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response
    
