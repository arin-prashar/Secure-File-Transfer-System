from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Crypto.Cipher import AES
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Setup
client = MongoClient(os.getenv("URI"), server_api=ServerApi('1'))
db = client["SecureFileTransfer"]

def decrypt_file(user: str, encrypted_file: str, output_file: str) -> None:
    """Decrypts an encrypted file using AES."""
    try:
        # Fetch key and nonce from the database
        user_record = db["senders"].find_one({"username": user})
        if not user_record:
            raise ValueError("No key found for the user.")

        key = user_record["key"]
        nonce = user_record["nonce"]

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        with open(encrypted_file, "rb") as enc_file:
            encrypted_data = enc_file.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        # Save decrypted file
        with open(output_file, "wb") as out_file:
            out_file.write(decrypted_data)

        print(f"File decrypted and saved as: {output_file}")
    except Exception as e:
        print(f"Error decrypting file: {e}")
        raise