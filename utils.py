import rsa

def GenetarteKeys():
    public_key, private_key = rsa.newkeys(1024)
    return public_key, private_key


def Sign(message, private_key):
   return rsa.sign(message, private_key, "SHA-256")
    

def Verify(message, signature, public_key):
    try:
        rsa.verify(message, signature, public_key)
        return True
    except:
        return False


""" if __name__ == "__main__":
    print("Main")
    public_key, private_key = rsa.newkeys(1024)
    sec, secKey = rsa.newkeys(1024)
    message = 'A message for signing'
    test = Sign(message.encode("utf-8"), private_key)
    print(Verify(message, test, public_key))
    print(Verify(message, test, sec)) """