import os
import socket
from dotenv import load_dotenv
load_dotenv()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



def main():
    # client=MongoClient(os.getenv("URI"),server_api=ServerApi('1'))    
    soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    soc.bind(("localhost",3000))
    soc.listen(5)
    print(soc)
    
    while True:
        client_socket,addr=soc.accept()
        print(client_socket,"|",addr)
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            print(f"Received: {data.decode()}")

            # Send response back to client
            client_socket.send("Hello, client!".encode())

        # Close client socket
        client_socket.close()
        print("client disconnected and shutdown")


main()