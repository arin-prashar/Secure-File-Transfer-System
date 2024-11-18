import socket
import random
import string
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Setup
client = MongoClient(os.getenv("URI"), server_api=ServerApi('1'))
db = client["SecureFileTransfer"]

def generate_otp():
    """Generates a secure OTP."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def save_otp_in_db(user, ip, port, otp):
    """Saves the OTP and sender info in the database."""
    try:
        db.senders.insert_one({"username": user, "ip": ip, "port": port, "otp": otp})
        print(f"Saved OTP for {user}: {otp}")
    except Exception as e:
        print(f"Error saving OTP in database: {e}")

def handle_client(client_socket, addr):
    """Handles communication with the client (sender or receiver)."""
    try:
        data = client_socket.recv(4096).decode().strip()
        print(f"Received data from {addr}: {data}")

        # Check if this is an OTP query or registration
        if ":" in data:  # Assume registration data contains a colon
            sender_info = eval(data)  # Assumes registration data is a stringified dictionary
            user = sender_info.get("user")
            port = sender_info.get("listening_port")

            # Generate OTP and save in the database
            otp = generate_otp()
            save_otp_in_db(user, addr[0], port, otp)

            # Send OTP back to sender
            client_socket.send(f"Your OTP is: {otp}".encode())
        else:  # Assume this is an OTP query
            otp = data
            sender_record = db.senders.find_one({"otp": otp})

            if sender_record:
                ip = sender_record["ip"]
                port = sender_record["port"]
                client_socket.send(f"{ip}:{port}".encode())  # Send IP:Port
            else:
                client_socket.send("Invalid OTP".encode())
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.send("Error occurred".encode())
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", int(os.getenv("PORT", 3000))))  # Use port from .env or default to 3000
    server_socket.listen(5)
    print("Main server is listening for connections...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            handle_client(client_socket, addr)
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()