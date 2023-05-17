# Import necessary libraries
import random
from utils import GenetarteKeys, Sign, Verify

NUMBER_OF_NODES = 0
public_keys_dict = {}
memPool = []
balance = {}
# Define the consensus algorithm function
def consensus_algorithm(nodes, blocks):
    # Select a block for validation
    block_to_validate = random.choice(blocks)
    
    # Choose the node to validate the block
    chosen_node = proof_of_stake(nodes)
    
    # Validate the block using practical byzantine fault tolerance
    is_valid = practical_byzantine_fault_tolerance(chosen_node, block_to_validate)
    
    # If the block is valid, add it to the blockchain and update nodes' balances
    if is_valid:
        blockchain.append(block_to_validate)
        update_balances(chosen_node, block_to_validate)
    else:
        # If the block is not valid, remove it from the list of blocks
        blocks.remove(block_to_validate)

# Define the proof of stake function
def proof_of_stake(nodes):
    # Calculate the total stake
    total_stake = sum([node.stake for node in nodes])
    
    # Choose a random number between 0 and the total stake
    random_number = random.uniform(0, total_stake)
    
    # Iterate over the nodes and subtract their stakes from the random number until it becomes negative
    for node in nodes:
        random_number -= node.stake
        if random_number < 0:
            return node
    
    # If the random number is not negative after iterating over all nodes, return the last node
    return nodes[-1]

# Define the practical byzantine fault tolerance function
def practical_byzantine_fault_tolerance(node, block):
    # Create a list of all the nodes except for the chosen node
    other_nodes = [n for n in nodes if n != node]
    
    # Create a list of the other nodes' responses to the block
    responses = [n.validate_block(block) for n in other_nodes]
    
    # Count the number of responses that match the chosen node's response
    matches = sum([response == node.validate_block(block) for response in responses])
    
    # If the number of matches is greater than 2/3 of the total number of nodes, return True
    return matches > len(nodes) * 2/3

# Define the Node class
class Node:
    def __init__(self, stake, balance):
        self.stake = stake
        self.balance = balance
        self.private_key, self.public_key = GenetarteKeys()
        self.id = NUMBER_OF_NODES + 1
        NUMBER_OF_NODES += 1
        public_keys_dict[self.id] = self.public_key
        balance[self.id] = self.balance

    
    def validate_block(self, block):
        # Placeholder function for block validation

        for transaction in block.transactions:
            pub_key = public_keys_dict[transaction.from_address]

            #verifty the signature of the transaction
            if Verify(transaction.value_byte, transaction.signature, pub_key) == False:
                return False
            #check if the sender has enough balance
            if transaction.value > balance[transaction.from_address]:
                return False
        return True
    
    def GenerateTransaction(self, to_address, value):
        
        message = str(self.id) + ":" + str(to_address) + ":" + str(value)

        # Sign the message using the private key of the sender

        signature = Sign(message.encode("utf-8"), self.private_key)

        # Create a transaction

        transaction = Transaction(self.id, to_address, value, signature, message)
        
        memPool.append(transaction)

class Transaction:
    def __init__(self, from_address, to_address, value, signature, value_byte):
        self.value = value
        self.from_address = from_address
        self.to_address = to_address
        self.signature = signature
        self.value_byte = value_byte



class Block:
    def __init__(self, transactions, prevHeader):
        self.trasactions = transactions
        self.prevHeader = prevHeader

# Create a list of nodes with different stakes
nodes = [Node(100), Node(50), Node(25), Node(10)]

# Create a list of blocks to choose from
blocks = []

# Create an empty blockchain
blockchain = []

# Run the consensus algorithm for a certain number of rounds
for i in range(len(nodes)):
    consensus_algorithm(nodes, blocks)
