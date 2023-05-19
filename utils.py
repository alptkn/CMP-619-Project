import rsa
from merkly.mtree import MerkleTree

def GenetarteKeys():
    public_key, private_key = rsa.newkeys(1024)
    return private_key, public_key


def Sign(message: bytes, private_key: rsa.PrivateKey) -> bytes:
   return rsa.sign(message, private_key, "SHA-256")
    

def Verify(message: bytes, signature: bytes, public_key: rsa.PublicKey) -> bool:
    try:
        rsa.verify(message, signature, public_key)
        return True
    except:
        return False


def ConstructMerkleTree(transactionList: list[str]) -> MerkleTree:
    mtree = MerkleTree(transactionList)
    return mtree


def VerifyMerkleTree(mtree: MerkleTree, node: str) -> bool:
    proof = mtree.proof(node)
    return mtree.verify(proof)


