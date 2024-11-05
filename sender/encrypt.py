from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
from dotenv import load_dotenv
load_dotenv()


uri = os.getenv('URI')

client=MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def generate_key(user:str)->None:
    key = get_random_bytes(16)
    nonce = get_random_bytes(16)
    try:
        client["SecureFileTransfer"]["users"].update_one({"username":user},{"$set":{"key":key,"nonce":nonce}},upsert=True)
    except Exception as e:
        print(e," \n1")

def encrypt_file(user:str, file_to_encrypt:str)->None:
    try:
        key = client["SecureFileTransfer"]["users"].find_one({"username":user})["key"]
        nonce = client["SecureFileTransfer"]["users"].find_one({"username":user})["nonce"]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        with open(file_to_encrypt, "rb") as file:
            encrypted_file, tag = cipher.encrypt_and_digest(file.read())
        return {encrypted_file, tag}
    except Exception as e:
        print(e," \n2")


client.close()