# llama_index_gui
llama index gui tool
python > 3.10
llama index：https://github.com/jerryjliu/llama_index.git
界面库部分参考;https://github.com/Akegarasu/ChatGLM-webui.git

# Features
通过 llama index加载自定义知识库给openai进行自有知识库问题回答

# install
pip install -r .\requirements.txt

# run
1、
修改chat_gui.py  build_gui.py  build.py 中的openai api  key
    #openai key
    os.environ["OPENAI_API_KEY"] = 'your openai key'
    #代理
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"

2、构建向量库
python  build_gui.py
或者
python  build.py

3、加载上下文，启动聊天程序，程序会根据向量库的内容回答问题
python  chat_gui.py