import ecdsa
import os

def generate_signing_key():
    signingKey = ecdsa.SigningKey.generate(ecdsa.NIST256p)

    with open('private' + ".pem", "wb") as f:
        f.write(signingKey.to_pem())

    with open('public' + ".pem", "wb") as f:
        f.write(signingKey.verifying_key.to_pem())

generate_signing_key()