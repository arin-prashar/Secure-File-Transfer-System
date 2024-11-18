import os
import pathlib
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from dotenv import load_dotenv
load_dotenv()


uri = os.getenv('URI')

client=MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def generate_key(user:str)->bool:
    key = get_random_bytes(16)
    nonce = get_random_bytes(16)
    try:
        client["SecureFileTransfer"]["senders"].update_one({"username":user},{"$set":{"key":key,"nonce":nonce}},upsert=True)
        return True
    except Exception as e:
        print(e," \n1")
        return False

def encrypt_file(user:str, file_to_encrypt:str)->dict:
    key = client["SecureFileTransfer"]["senders"].find_one({"username":user})["key"]
    nonce = client["SecureFileTransfer"]["senders"].find_one({"username":user})["nonce"]
    try:
        file_to_encrypt=pathlib.Path(file_to_encrypt)
        print(file_to_encrypt)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        with open(file_to_encrypt, "rb") as file:
            encrypted_file, tag = cipher.encrypt_and_digest(file.read())
        # print(encrypted_file)
        return {encrypted_file, tag}
    except Exception as e:
        print(e," \n2")
        raise ValueError("")
    
encrypt_file("asd","Shared_Files/Beach-Dark.png")