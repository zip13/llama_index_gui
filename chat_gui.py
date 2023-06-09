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


def init():
    ini_env()
    load_index()


def main():
    while True:
        ui = create_ui()
        ui.launch(share=True,server_port=cmd_opts.port,server_name="0.0.0.0" if cmd_opts.listen else None)

if __name__ == "__main__":
    init()
    main()
