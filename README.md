# Llama Index GUI 工具
[English](./README.en.md) | 简体中文

本项目利用 Llama Index（GPT Index） 和 Python 构建一个定制的知识库，使 OpenAI 能够回答来自该知识库的问题。它提供了一个图形用户界面（GUI），用于可视化从知识库构建向量库，以及一个基于本地构建的知识库进行问题回答的聊天界面。该工具开发使用的 Python 版本高于 3.10，建议使用 Conda 进行环境配置。

Llama Index 的源代码可以在这里找到：https://github.com/jerryjliu/llama_index.git
GUI 部分参考了这个项目：https://github.com/Akegarasu/ChatGLM-webui.git

## 功能
- 通过 Llama Index 加载自定义知识库，使 OpenAI 能够回答来自这个知识库的问题。
- `build_gui.py` 脚本提供了一种可视化方式，用于从知识库构建向量库。
- `chat_gui.py` 脚本提供了一个聊天界面，该界面使用已构建的向量库回答问题。

## 安装
使用以下命令安装必要的包：
```
pip install -r requirements.txt
```

## 环境配置
在 `env.py` 文件中设置环境变量：

```python
# OpenAI API 密钥
os.environ["OPENAI_API_KEY"] = 'your openai key'

# 代理设置
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"
```

## 使用方法

1. **构建向量库**

   您可以使用 `build_gui.py` 脚本可视化地构建向量库，或者使用 `build.py` 脚本在命令行中构建。运行以下命令之一：

    ```
    python build_gui.py
    ```
    或者

    ```
    python build.py
    ```

2. **加载上下文并启动聊天程序**

   一旦向量库构建完成，您可以加载上下文并启动聊天程序。这将使系统能够根据向量库的内容回答问题。使用以下命令启动：

    ```
    python chat_gui.py
    ```

尽情享受您的定制化 AI 助手吧！
