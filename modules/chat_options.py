import argparse

parser = argparse.ArgumentParser()

#llama index param
parser.add_argument("--persist_dir", help="evaluate at this precision", type=str, default="./storage")

#openai param
parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo")
parser.add_argument("--num_output", type=int, default="1024")
parser.add_argument("--chunk_size_limit", type=int, default="1024")
parser.add_argument("--max_chunk_overlap", type=int, default="20")
parser.add_argument("--max_input_size", type=int, default="4096")
parser.add_argument("--similarity_top_k", type=int, default="3")
parser.add_argument("--temperature", type=float, default="0")

#gradio param
parser.add_argument("--port", type=int, default="17860")
parser.add_argument("--listen", action='store_true', help="launch gradio with 0.0.0.0 as server name, allowing to respond to network requests")
parser.add_argument("--share", action='store_true', help="use gradio share")

cmd_opts = parser.parse_args()
need_restart = False
