import threading
from .routes import *

def init():
    command.initialize_client()
    server_thread = threading.Thread(target=command.initialize_server)
    server_thread.daemon = True
    server_thread.start()


