from Cryptodome.Cipher import AES
import json
import jsonpickle

key = b'IPNHZjt0ag5EERvI'

def encode(data, file_name):
    data_fixed = jsonpickle.encode(data).encode("utf8")
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data_fixed)

    file_out = open(file_name + ".bin", "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()

def decode(file_name):
    file_in = open(file_name + ".bin", "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)   
    return jsonpickle.decode(data.decode("utf8"))