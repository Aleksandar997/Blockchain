import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

HOST = os.getenv('HOST')
INIT_PORT = int(os.getenv('INIT_PORT'))
CLIENT_PORT = int(os.getenv('CLIENT_PORT'))
BLOCKCHAIN_PORT = int(os.getenv('BLOCKCHAIN_PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))
MAXIMUM_CONNECTIONS = int(os.getenv('MAXIMUM_CONNECTIONS'))
PEER_CACHE_NAME=os.getenv('PEER_CACHE_NAME')
BLOCKCHAIN_CACHE_NAME=os.getenv('BLOCKCHAIN_CACHE_NAME')
