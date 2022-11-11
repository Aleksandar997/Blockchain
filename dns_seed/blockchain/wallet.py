import ecdsa
import os

def generate_signing_key():
    signingKey = ecdsa.SigningKey.generate(ecdsa.NIST256p)

    with open("private_key.pem", "wb") as f:
        f.write(signingKey.to_pem())

    with open("public_key.pem", "wb") as f:
        f.write(signingKey.verifying_key.to_pem())

def read_signing_key():
    if os.path.isfile("private_key.pem") == False:
        return None
    with open("private_key.pem", "r") as f:
        signing_key = ecdsa.SigningKey.from_pem(f.read())
    return signing_key

def read_public_key(signing_key):
    if os.path.isfile("public_key.pem") == False:
        return None
    with open("public_key.pem", "r") as f:
        public_key = signing_key.verifying_key.from_pem(f.read()).to_string("uncompressed").hex()
    return public_key

def read_keys():
    signing_key = read_signing_key()
    public_key = read_public_key(signing_key)
    return (signing_key, public_key)
    