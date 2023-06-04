# Import necessary libraries
import random
import hashlib
from utils import GenetarteKeys, Sign, Verify
from model import Node, blockchain, Block, balances, memPool
import time


def consensus_algorithm(nodes):
    
    chosen_node = proof_of_stake(nodes)
    block_to_validate = chosen_node.Mine()
    
    is_valid = practical_byzantine_fault_tolerance(chosen_node, block_to_validate)
    
    
    if is_valid:
        blockchain.append(block_to_validate)

        update_balances(block_to_validate)
        
   


def proof_of_stake(nodes: list[Node]) -> Node:
   
    total_stake = sum([node.stake for node in nodes])
    
    
    random_number = random.uniform(0, total_stake)
    
   
    for node in nodes:
        random_number -= node.stake
        if random_number < 0:
            return node
    
    
    return nodes[-1]

# Define the practical byzantine fault tolerance function
def practical_byzantine_fault_tolerance(node, block):
    
    other_nodes = [n for n in nodes if n != node]
    
    
    responses = [n.validate_block(block) for n in other_nodes]
    
   
    matches = sum([response == node.validate_block(block) for response in responses])
    
    
    return matches > len(nodes) * 2/3

# Define the Node class
def update_balances(block: Block) -> None:

    for traansaction in block.transactions:
        
        balances[traansaction.from_address] -= traansaction.value
        balances[traansaction.to_address] += traansaction.value
    
    return None





if __name__ == "__main__":

    nodes = [Node(100, 200), Node(50, 120), Node(25, 100), Node(10, 70)]

    start = time.time()
    nodes[0].GenerateTransaction(nodes[1].id, 50)
    nodes[0].GenerateTransaction(nodes[2].id, 50)
    nodes[2].GenerateTransaction(nodes[3].id, 50)
    nodes[3].GenerateTransaction(nodes[0].id, 20)

    consensus_algorithm(nodes)

    nodes[0].GenerateTransaction(nodes[2].id, 30)
    nodes[0].GenerateTransaction(nodes[3].id, 20)
    nodes[2].GenerateTransaction(nodes[3].id, 50)
    nodes[3].GenerateTransaction(nodes[1].id, 20)

    consensus_algorithm(nodes)

    end = time.time()

    print("Time taken: ", end - start)






""" for i in range(len(nodes)):
    consensus_algorithm(nodes, blocks) """
