import hashlib
import json
from datetime import date

class Block:
    def json_default(self, value):
        if isinstance(value, date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

    def calculate_hash(self) -> str:
        transactionJson = json.dumps(self.transaction, default=lambda value: self.json_default(value.get_hashable_props())) 
        return hashlib.sha256((self.previous_hash + str(self.timestamp) + transactionJson + str(self.nonce)).encode('utf-8')).hexdigest()

    def __init__(self, transaction, previous_hash = '', timestamp = date.today()) -> None:
        self.hashLen = 64
        self.nonce = 0
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash if previous_hash != '' else '0' * self.hashLen
        self.hash = self.calculate_hash()

    def mine_block(self, difficulty) -> None:
        while str(self.hash[0: difficulty]) != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        

    
