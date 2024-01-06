from examples.hello import AppMain
# from utils.pico_run import run
from utils.fast_server import run
from utils.find_port import find_available_port

# python usage.py

if __name__ == "__main__":
    port = find_available_port(port_min=5000)
    run(AppMain, port=port)
