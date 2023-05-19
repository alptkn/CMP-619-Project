import hashlib
from utils import GenetarteKeys, Sign, Verify
from merkly.mtree import MerkleTree
import json
import datetime
import uuid


NUMBER_OF_NODES = 0
GENESIS_BLOCK_MESSAGE = "This is the genesis block!"
public_keys_dict = {}
memPool = []
balances = {}
blockchain = []
#proposed_block = None


# Define the Transaction class
class Transaction:
    def __init__(self, from_address: int, to_address: int, value, signature: bytes, message: str):
        self.value = value
        self.from_address = from_address
        self.to_address = to_address
        self.signature = signature
        self.message = message


#Define the Block class
class Block:
    def __init__(self, transactionList: list[Transaction], prevHeader: str):
        transaction_message = []
        for item in transactionList: 
            transaction_message.append(item.message)

        self.mtree = MerkleTree(transaction_message)
        self.prevHeader = prevHeader
        self.mRoot = self.mtree.root
        self.timestamp = str(datetime.datetime.now())
        self.transactions = transactionList
        self.id = str(uuid.uuid4())
    
    def ComputeHash(self) -> str:
        block = {
            "id": self.id,
            "merkleRoot": self.mRoot,
            "prevHeader": self.prevHeader,
            "timestamp": self.timestamp
        }

        encoded_block = json.dumps(block, sort_keys=True).encode("utf-8")
        
        return hashlib.sha256(encoded_block).hexdigest()

# Define the Node class
class Node:
    def __init__(self, stake, balance):
        self.stake = stake
        self.balance = balance
        self.private_key, self.public_key = GenetarteKeys()
        global NUMBER_OF_NODES
        self.id = NUMBER_OF_NODES + 1
        NUMBER_OF_NODES += 1
        public_keys_dict[self.id] = self.public_key
        balances[self.id] = self.balance

    
    def validate_block(self, block):
        # Placeholder function for block validation

        for transaction in block.transactions:
            pub_key = public_keys_dict[transaction.from_address]

            #verifty the signature of the transaction
            if Verify(transaction.message.encode('utf-8'), transaction.signature, pub_key) == False:
                return False
            #check if the sender has enough balance
            if transaction.value > balances[transaction.from_address]:
                return False
        return True
    
    def GenerateTransaction(self, to_address, value):
        
        message = str(self.id) + ":" + str(to_address) + ":" + str(value)

        # Sign the message using the private key of the sender

        signature = Sign(message.encode("utf-8"), self.private_key)

        # Create a transaction

        transaction = Transaction(self.id, to_address, value, signature, message)
        
        memPool.append(transaction)

        return
    
    def Mine(self) -> Block:
        transactionList = []
        global memPool
        for transaction in memPool:

            pub_key = public_keys_dict[transaction.from_address]
            if Verify(transaction.message.encode('utf-8'), transaction.signature, pub_key) == False:
                continue

            if transaction.value > balances[transaction.from_address]:
                continue
        
            transactionList.append(transaction)                
        
        if len(blockchain) == 0:
            hashed_message = hashlib.sha256(GENESIS_BLOCK_MESSAGE.encode("utf-8")).hexdigest()
            block = Block(transactionList, hashed_message)
        
        else: 
            prevHeader = blockchain[len(blockchain) - 1].ComputeHash()
            block = Block(transactionList, prevHeader)

        memPool = []
        return block
    
        




