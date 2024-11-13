import os
import urllib
import pathlib
import sys
import socket
from dotenv import load_dotenv
load_dotenv()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# import receiver.decrypt as decrypt
# import receiver.fileInfo as fi


def receive_file():
    soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    soc.connect(("localhost",3000))
    soc.send("Hello, server!".encode())
    print(soc)
    pass






def main():
    print(os.getenv("port"),os.getenv("host"))

    # client=MongoClient(os.getenv("URI",server_api=ServerApi('1')))
    receive_file()

main()