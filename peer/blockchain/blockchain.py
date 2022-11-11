from .block import Block
from .transaction import Transaction, Transaction_view

class Blockchain:
    difficulty = 2
    def __init__(self) -> None:
        self.transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        block = Block(self.transactions)
        block.mine_block(self.difficulty)
        self.chain.append(block)       
        self.transactions = []

    def get_latest_block(self) -> Block:
        return self.chain[len(self.chain) - 1]

    def create_block(self):
        block = Block(self.transactions, self.get_latest_block().hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)

    def validate_chain(self) -> bool:
        invalid_blocks = []
        for i, block in enumerate(self.chain):
            if i == 0:
                continue
            previous_block = self.chain[i - 1]
            
            if block.hash != block.calculate_hash():
                invalid_blocks.append(self.chain.pop(i))

            if block.previous_hash != previous_block.hash:
                invalid_blocks.append(self.chain.pop(i))
            
            for tran in block.transaction:
                if (tran.is_valid() == False):
                    invalid_blocks.append(self.chain.pop(i))

            return invalid_blocks

    def mine_block(self, signingKey):
        transaction = Transaction(56 * '0', signingKey.verifying_key.to_string("uncompressed").hex(), 1)
        transaction.sign_transaction(signingKey, True)
        self.transactions = map(lambda t: t.publish, self.transactions)
        self.transactions.insert(0, transaction)
        self.create_block()
        self.transactions = []
        self.validate_chain()
        self.save_blockchain_on_disk()
        return self.get_latest_block()

    def add_transaction(self, signingKey, receiver, amount):
        transaction = Transaction(signingKey.verifying_key.to_string("uncompressed").hex(), receiver, amount)
        transaction.sign_transaction(signingKey)
        self.transactions.append(transaction)
        return transaction.id

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            for tran in block.transaction:
                if tran.from_address == address:
                    balance -= tran.amount
                elif tran.to_address == address:
                    balance += tran.amount
        return balance

    def list_pending_transactions_by_address(self, address):
        transactions = list(
                            map(
                                 lambda t: Transaction_view(t.from_address, t.to_address, t.amount, t.timestamp, t.id).serialize_pending(), 
                                 filter(
                                     lambda f: f.from_address == address or f.to_address == address,
                                     self.transactions
                                 )
                                )
                            )
        return transactions

    def list_all_transactions_by_address(self, address):
        transactions = {
            "pending": self.list_pending_transactions_by_address(address),
            "completed": self.list_completed_transactions_by_address(address)
        }
        return transactions

    def list_completed_transactions_by_address(self, address):
        transactions = []
        for block in self.chain:
            for tran in block.transaction:
                if (tran.from_address == address or tran.to_address == address):
                    transactions.append(Transaction_view(tran.from_address, tran.to_address, tran.amount, tran.timestamp).serialize())

        return transactions

    def append_chain(self, block):
        if block in self.chain:
            return
        self.chain.append(block)
        self.validate_chain()
        self.save_blockchain_on_disk()

    def append_transaction(self, transaction):
        if transaction in self.transactions:
            return
        self.transactions.append(transaction)

    def append_chain_bulk(self, blockchain):
        self.chain = blockchain.chain
        self.transactions = blockchain.transactions
        self.validate_chain()
        self.save_blockchain_on_disk()

    def remove_pending_transaction(self, id):
        self.transactions = list(filter(lambda t: t.id != id, self.transactions))


    
