from llama_index import ServiceContext, LLMPredictor, PromptHelper,StorageContext, load_index_from_storage
from langchain import OpenAI
from modules.chat_options import cmd_opts
from modules.context import Context
import gradio as gr
import os



css = "style.css"
script_path = "scripts"
_gradio_template_response_orig = gr.routes.templates.TemplateResponse


index=None
first = True

def load_index():
    global index
     # LLM Predictor (gpt-3.5-turbo)
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=cmd_opts.temperature, model_name=cmd_opts.model_name, streaming=True))
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

def chat(ctx, message, model_type):
    global index,first
    if not index:
        raise "index not loaded"
    ctx.limit_round()
  
    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=cmd_opts.similarity_top_k,
        response_mode=model_type
    )

    if first:
        response_stream = query_engine.query(message+',请用中文回答')
    else:
        response_stream = query_engine.query(message)

    response = response_stream.get_response()
    print(response)
    ctx.append(message, response.response)
    ctx.refresh_last()
    return ctx.rh

# def save(ctx):
#     pyperclip.copy("\n".join([f"User: {q}\nBot: {a}" for q, a in ctx.rh]))

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
                    default="tree_summarize",  # 使用第一个选项作为默认值
                )
                submit = gr.Button("发送", elem_id="c_generate")
        
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(elem_id="c_chatbot", show_label=False).style(height=500)
                savebutton = gr.Button("保存", elem_id="c_save")
        #设置一个对话窗
        submit.click(chat, inputs=[
                state,
                input,
                model_type
                
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
    
