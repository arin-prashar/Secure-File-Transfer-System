import os
import pathlib
import sys
import socket
from dotenv import load_dotenv
load_dotenv()

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



























def main():
    fileSelect()