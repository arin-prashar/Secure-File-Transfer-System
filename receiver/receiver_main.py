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


def receive_fille():
    # soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # soc.connect((os.getenv("host"), os.getenv("port")))
    pass






def main():
    print(os.getenv("port"),os.getenv("host"))

    # client=MongoClient(os.getenv("uri",server_api=ServerApi('1')))
    receive_fille()

main()