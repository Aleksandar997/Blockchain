from blockchain.blockchain import Blockchain
from environment import *
import pickle
import datetime
from common.crypto import decode, encode
from common.peer import PeerList, Peer
from common.socket import Sockets
import select
import socket

def initialize_server():
    peers = PeerList()
    blockchain = Blockchain()
    sockets = Sockets()

    if os.path.isfile(PEER_CACHE_NAME + '.bin'):
        peers = decode(PEER_CACHE_NAME)

    if os.path.isfile(BLOCKCHAIN_CACHE_NAME + '.bin'):
        blockchain = decode(BLOCKCHAIN_CACHE_NAME)

    for item in INIT_PORT, BLOCKCHAIN_PORT:
        sockets.append_socket(HOST, item, MAXIMUM_CONNECTIONS)

    while True:
        read, _, _ = select.select(sockets.get_sockets(), [], [])

        for r in read:
            for item in sockets:
                if r == item['socket']:
                    connection, client_address = item['socket'].accept()
                    address = client_address[0]
                    if item['port'] == INIT_PORT:
                        peers.remove_inactive_peers()
                        
                        peer = peers.append_peer(address)
                        encode(peers, PEER_CACHE_NAME)
                        if (peer != None and peer.address != address):
                            sync_top_peer(peer.address, client_address)
                            connection.send(pickle.dumps({'peer': peer.address, 'blockchain': blockchain}))
                        else:
                            connection.send(pickle.dumps({'peer': None, 'blockchain': blockchain}))

                    elif item['port'] == BLOCKCHAIN_PORT:
                        data_bytes = b""

                        while True:
                            try:
                                packet = connection.recv(1024)
                                if not packet: break
                                data_bytes += packet
                            except Exception as ex:
                                ValueError(ex)

                        res = pickle.loads(data_bytes)

                        blockchain.chain.append(res)
                        blockchain.validate_chain()
                        encode(blockchain, BLOCKCHAIN_CACHE_NAME)

def sync_top_peer(previous_peer, latest_peer):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((previous_peer, CLIENT_PORT))   
    client_socket.send('peer')
    client_socket.send(latest_peer)

def main():
    while True:
        try:
            initialize_server()
        except Exception as e:
            print(e)
            break


main()


*
* * * * * * * * * *