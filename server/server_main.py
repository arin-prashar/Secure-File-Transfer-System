import os
import socket
from dotenv import load_dotenv
load_dotenv()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



def main():
    client=MongoClient(os.getenv("uri"),server_api=ServerApi('1'))
    print(os.getenv("port"))
    soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # soc.bind(("",os.getenv("port")))