# Llama Index GUI Tool
English | [简体中文](./README.md)

This project utilizes the Llama Index（GPT Index）、ChatGPT and Python to build a custom knowledge base for OpenAI to answer questions from. It offers a graphical user interface (GUI) for visualizing the construction of the vector library from the knowledge base, as well as a chatting interface for question-answering based on the locally built knowledge base. This tool is developed with Python versions higher than 3.10, and it's recommended to use Conda for environment configuration.

Source code for the Llama Index can be found here: https://github.com/jerryjliu/llama_index.git
The GUI was built with some inspiration from here: https://github.com/Akegarasu/ChatGLM-webui.git

## Features
- Load custom knowledge bases through the Llama Index for OpenAI to answer questions from.
- The `build_gui.py` script provides a visual way to build a vector library from the knowledge base.
- The `chat_gui.py` script offers a chatting interface that uses the built vector library to answer questions.

## Installation
Install the necessary packages with the following command:
```
pip install -r requirements.txt
```

## Environment Configuration
Set your environment variables in the `env.py` file:

```python
# OpenAI API Key
os.environ["OPENAI_API_KEY"] = 'your openai key'

# Proxy settings
os.environ["http_proxy"] = "http://127.0.0.1:1080"
os.environ["https_proxy"] = "http://127.0.0.1:1080"
```

## Usage

1. **Build the Vector Library**

   You can build the vector library either visually using `build_gui.py` or through command line using `build.py` script. Run one of the following commands:

    ```
    python build_gui.py
    ```
    or

    ```
    python build.py
    ```

2. **Load the Context and Start the Chat Program**

   Once the vector library is built, you can load the context and start the chat program. This will allow the system to answer questions based on the content of the vector library. Use the following command to start:

    ```
    python chat_gui.py
    ```

Enjoy your custom-built AI assistant!
