import os
import sys
import socket
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import encrypt as encrypt
import fileInfo as fi

load_dotenv()

def fileSelect():
    print("Please drop the files into the Shared Files Folder\nYou want to share.")
    print("We suggest 1 at a time for better performance.")
    try:
        os.listdir("Shared_Files")
    except FileNotFoundError:
        os.mkdir("Shared_Files")

    Y_N = input("Is the file in the Shared Files Folder? (Y/N): ")
    if Y_N.lower() == "n":
        print("Please drop the file into the Shared Files Folder and rerun the program.")
        sys.exit()

    files = os.listdir("Shared_Files")
    print("Files in the Shared Files Folder:")
    for i in range(len(files)):
        print(f"{i+1}. {files[i]}")
    
    choice = int(input("Enter the number of the file you want to send: "))
    return "Shared_Files/"+files[choice - 1]

def registerWithMainServer(user, listening_port):
    """Registers sender with the main server and receives OTP."""
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((os.getenv("host"), int(os.getenv("port"))))
        print("Connected to the main server.")

        # Send registration data to main server
        registration_data = {
            "user": user,
            "listening_port": listening_port
        }
        soc.send(str(registration_data).encode())

        # Receive OTP from server
        otp = soc.recv(4096).decode()
        print(f"Received OTP from server: {otp}")

        # soc.close()
        return otp
    except Exception as e:
        print(f"Error connecting to the main server: {e}")
        return None

def startListeningServer(file_path):
    """Starts a server to accept a connection from the receiver."""
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(("0.0.0.0", 0))  # Bind to any available port
        listening_port = soc.getsockname()[1]
        print(f"Listening for connections on port {listening_port}")
        return soc, listening_port
    except Exception as e:
        print(f"Error starting listening server: {e}")
        sys.exit()

def handleReceiverConnection(soc, file_path):
    """Handles the file transfer to the receiver."""
    try:
        soc.listen(1)
        print("Waiting for receiver to connect...")
        client_socket, addr = soc.accept()
        print(f"Receiver connected from {addr}")

        # Encrypt and send the file
        encrypted_file = encrypt.encrypt_file("user", file_path)
        file_info=fi.get_file_info(file_path)
        client_socket.send(str(file_info)[1:-1].encode())
        client_socket.sendall(encrypted_file[0].encode())
        client_socket.send("<END>")
        print("File sent successfully.")
        client_socket.close()
    except Exception as e:
        print(f"Error during file transfer: {e}")
    finally:
        soc.close()

def main():
    # MongoDB setup (if needed)
    client = MongoClient(os.getenv("URI"), server_api=ServerApi('1'))

    # File selection
    file_name = fileSelect()
    file_path = os.path.join("Shared_Files", file_name)

    # Start a listening server
    soc, listening_port = startListeningServer(file_path)

    # Register with the main server
    user = input("Enter your username: ")

    if encrypt.generate_key(user):
        print("generated")
        registerWithMainServer(user, listening_port)
    else:
        sys.exit("1")
    # Wait for receiver and handle the file transfer
    handleReceiverConnection(soc, file_path)

if __name__ == "__main__":
    main()
