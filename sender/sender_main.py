import os
import urllib
import pathlib
import sys
import socket
from dotenv import load_dotenv
load_dotenv()

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import sender.encrypt as encrypt
import sender.fileInfo as fi

def fileSelect():
    print("Please drop the files into the Shared Files Folder\nYou want to share.")
    print("We suggest 1 at a time for better performance.")
    try:
        os.listdir("Shared_Files")
    except FileNotFoundError:
        os.mkdir("Shared_Files")

    Y_N=input("Is the file in the Shared Files Folder? (Y/N): ")
    if Y_N.lower() == "n":
        print("Please drop the file into the Shared Files Folder and rerun the program.")
        sys.exit()

    files = os.listdir("Shared_Files")
    print("Files in the Shared Files Folder:")
    for i in range(len(files)):
        print(f"{i+1}. {files[i]}")

def sendFile(user:str, file:str):
    client=MongoClient(os.getenv("uri",server_api=ServerApi('1')))
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(os.getenv("port"),os.getenv("host"))
    socket.connect((os.getenv("host"), os.getenv("port")))
    print("Connected to the server.")
    print("Sending file...")
    file = fi.FileInfo(file)
    file.encrypt()
    file.send(socket)
    print("File sent.")
    socket.close()
















def main():
    # client=MongoClient(os.getenv("uri",server_api=ServerApi('1')))
    fileSelect()