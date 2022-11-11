import os
from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(".env")

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
DNS_SEED_HOST = os.getenv('DNS_SEED_HOST')
DNS_SEED_INIT_PORT = int(os.getenv('DNS_SEED_INIT_PORT'))
DNS_SEED_BLOCKCHAIN_PORT = int(os.getenv('DNS_SEED_BLOCKCHAIN_PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))
MAXIMUM_CONNECTIONS = int(os.getenv('MAXIMUM_CONNECTIONS'))
API_PORT = int(os.getenv('API_PORT'))

__HOME = os.environ['APPDATA']

__DATA_FOLDER_NAME = os.getenv('DATA_FOLDER_NAME')
DATA_FOLDER_PATH = os.path.join(__HOME, __DATA_FOLDER_NAME)

PRIVATE_KEY_FILE_NAME = os.path.join(DATA_FOLDER_PATH, os.getenv('PRIVATE_KEY_FILE_NAME'))
PUBLIC_KEY_FILE_NAME = os.path.join(DATA_FOLDER_PATH, os.getenv('PUBLIC_KEY_FILE_NAME'))