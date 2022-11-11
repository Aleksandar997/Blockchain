from .blockchain_service import BlockchainService
from .network import Network
import blockchain.wallet as wallet
from .common.helper import exec
from .common.logger import LoggerService
from environment import DATA_FOLDER_PATH
from .common.crypto import decode, encode
import os

class Command:
    def __init__(self):
        keys = wallet.read_keys()
        self.signing_key = keys[0]
        self.public_key = keys[1]

        self.network = Network()

    def __validate_wallet(self):
        keys = wallet.read_keys()
        self.signing_key = keys[0]
        if (self.signing_key == None):
            raise AttributeError('Please generate a wallet!')

    def save_blockchain_on_disk(self):
        encode(BlockchainService.blockchain, DATA_FOLDER_PATH)

    def load_blockchain_from_disk(self):
        if os.path.isfile(DATA_FOLDER_PATH + '.bin'):
            BlockchainService.blockchain = decode(DATA_FOLDER_PATH)

    def list_pending_transactions(self):
        def __list_pending_transactions():
            self.__validate_wallet()
            return BlockchainService.blockchain.list_pending_transactions_by_address(self.public_key)
        return exec(__list_pending_transactions)

    def list_completed_transactions(self):
        def __list_completed_transactions():
            self.__validate_wallet()
            return BlockchainService.blockchain.list_completed_transactions_by_address(self.public_key)
        return exec(__list_completed_transactions)

    def list_all_transactions(self):
        def __list_all_transactions():
            self.__validate_wallet()
            return BlockchainService.blockchain.list_all_transactions_by_address(self.public_key)
        return exec(__list_all_transactions)

    def list_transactions_by_address(self, address):
        def __list_transactions_by_address():
            return BlockchainService.blockchain.list_completed_transactions_by_address(address)
        return exec(__list_transactions_by_address)

    def add_transaction(self, receiver, amount):
        def __add_transaction():
            self.__validate_wallet()
            if (receiver == None):
                raise AttributeError('Please add a receiving wallet!')
            if (amount == None):
                raise AttributeError('Please add a amount!')
            id = BlockchainService.blockchain.add_transaction(self.signing_key, receiver, amount)
            self.save_blockchain_on_disk()
            self.network.sync_transaction(id)
            return {
                "message": "Transaction successfully added",
                "data": id  
            }
        return exec(__add_transaction)

    def remove_pending_transaction(self, id):
        def __remove_pending_transaction():
            self.__validate_wallet()
            if (id == None):
                raise AttributeError('Please add a id!')
            BlockchainService.blockchain.remove_pending_transaction(id)
            self.save_blockchain_on_disk()
            return 'Transaction successfully removed'
        return exec(__remove_pending_transaction)

    def generate_wallet(self):
        def __generate_wallet():
            wallet.generate_signing_key()
            return 'Wallet generated successfully'
        return exec(__generate_wallet)

    def mine(self):
        def __mine():
            self.__validate_wallet()
            block = BlockchainService.blockchain.mine_block(self.signing_key)
            self.save_blockchain_on_disk()
            self.network.sync_block(block)
            return 'Block mined successfully'
        return exec(__mine)

    def check_balance(self):
        def __check_balance():
            return BlockchainService.blockchain.get_balance_of_address(self.public_key)
        return exec(__check_balance)

    def initialize_server(self):
        try_count = 0
        while try_count < 5:
            try:
                self.network.initialize_server()
            except:
                # LoggerService.logger.log_exception(e)
                self.load_blockchain_from_disk()
                try_count = try_count + 1
        
    def initialize_client(self):
        try_count = 0
        while try_count < 5:
            try:  
                self.network.initialize_client()
            except:
                # LoggerService.logger.log_critical(cre.characters_written)
                self.load_blockchain_from_disk()
                try_count = try_count + 1                

        