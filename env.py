import os
import sys
import logging
def ini_env():
    #openai key
    os.environ["OPENAI_API_KEY"] = 'your open api key'
    #代理
    os.environ["http_proxy"] = "http://127.0.0.1:1080"
    os.environ["https_proxy"] = "http://127.0.0.1:1080"
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
