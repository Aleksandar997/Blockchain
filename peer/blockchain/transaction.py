from datetime import date
import os
import hashlib
import uuid

class Transaction_view:
    def __init__(self, from_address, to_address, amount, timestamp, id = None) -> None:
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = timestamp
        self.id = id

    def serialize(self):
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def serialize_pending(self):
        return {
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'id': self.id
        }


class Transaction:
    def __init__(self, from_address, to_address, amount) -> None:
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = date.today()
        self.signature = bytearray()
        self.verifying_key = None

    def publish(self, transaction_pending):
        self.from_address = transaction_pending.from_address
        self.to_address = transaction_pending.to_address
        self.amount = transaction_pending.amount
        self.timestamp = transaction_pending.timestamp
        self.signature = transaction_pending.signature
        self.verifying_key = transaction_pending.verifying_key
        return self

    def get_hashable_props(self):
        return type('',(),{'from_address': self.from_address, 'to_address': self.to_address, 'amount': self.amount, 'timestamp': str(self.timestamp)})()

    def calculate_hash(self) -> str:
        return hashlib.sha256((self.from_address + self.to_address + str(self.amount) + str(self.timestamp)).encode('utf-8')).digest()

    def sign_transaction(self, signingKey, is_genesis_block = False):
        publicKey = signingKey.verifying_key.to_string("uncompressed").hex()
        self.verifying_key = signingKey.verifying_key
        if ((is_genesis_block == False and publicKey != self.from_address) or (is_genesis_block and publicKey != self.to_address)):
            return os.error('You cannot sign transactions for other wallets!')
        sign = signingKey.sign(self.calculate_hash())
        self.signature = sign

    def is_valid(self):
        if self.from_address == None:
            return True
        if self.signature == None or len(self.signature) == 0:
            return False
        return self.verifying_key.verify(self.signature, self.calculate_hash())

    def to_string(self):
        return ('from {0} to {1} amount {2}\\n', self.from_address, self.to_address, self.amount)
        
