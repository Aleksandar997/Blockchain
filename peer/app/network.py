import socket
from blockchain.block import Block
from environment import *
import pickle
from requests import get
from .blockchain_service import BlockchainService
from .common.logger import LoggerService

class Network:
    def __init__(self):
        self.queued_requests = []
        self.previous_peer = None
        self.latest_peer = None
        # self.ip = get('https://api.ipify.org').text
        # self.ip = '192.168.0.14'

    def initialize_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAXIMUM_CONNECTIONS)
        while True:
            connection, client_address = server_socket.accept()
            res = self.__receive_packet(connection)
            if (client_address in [q.address for q in self.queued_requests]) == False:
                self.queued_requests.append({'address': client_address, 'type': res})
                continue
            queued = [q for q in self.queued_requests if q.address == client_address][0]
            index = self.queued_requests.index(queued)
            if (queued.type == 'block'):
                BlockchainService.blockchain.append_chain(res)
                self.__sync_block_peer(self.previous_peer, res)
            elif (queued.type == 'transaction'):
                BlockchainService.blockchain.add_transaction()
                self.__sync_transaction_peer(self.previous_peer, res)
            elif (queued.type == 'peer'):
                self.latest_peer = res
            self.queued_requests.pop(index)


    def initialize_client(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.connect((DNS_SEED_HOST, DNS_SEED_INIT_PORT))
        res = self.__receive_packet(client_socket)

        self.previous_peer = res['peer']
        if res['blockchain']:
            BlockchainService.blockchain.append_chain_bulk(res['blockchain'])

    def sync_block(self, block: Block):
        self.__sync_block_peer(self.latest_peer, block)
        self.__sync_block_seed(block)

    def sync_transaction(self, id):
        transaction = [tran for tran in BlockchainService.blockchain.transactions if tran.id == id][0]
        self.__sync_transaction_peer(self.latest_peer, transaction)

    

    def __sync_block_seed(self, block: Block):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((DNS_SEED_HOST, DNS_SEED_BLOCKCHAIN_PORT))        
        client_socket.send(pickle.dumps(block))

    def __sync_block_peer(self, peer: str, block: Block):
        if (peer == None):
            return
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer, PORT))        
        client_socket.send('block')
        client_socket.send(pickle.dumps(block))

    def __sync_transaction_peer(self, peer: str, transaction):
        if (peer == None):
            return
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer, PORT))        
        client_socket.send('transaction')
        client_socket.send(pickle.dumps(transaction))

    def __receive_packet(self, socket: socket.socket):
        data_bytes = b""
        current_packet_size = 0
        while True:
            try:
                packet = socket.recv(BUFFER_SIZE)
                current_packet_size = len(packet)
                data_bytes += packet
                print(current_packet_size)
                if (current_packet_size < BUFFER_SIZE):
                    break
            except Exception as ex:
                ValueError(ex)

        return pickle.loads(data_bytes)   