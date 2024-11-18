import os
import socket
import tqdm
from dotenv import load_dotenv
from decrypt import decrypt_file

load_dotenv()

def query_main_server_for_sender(otp):
    """Queries the main server with the OTP to get the sender's IP and port."""
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_server_address = (os.getenv("host"), int(os.getenv("port")))  # Main server's address
        soc.connect(main_server_address)
        print("Connected to the main server.")

        # Send OTP to main server
        soc.send(otp.encode())
        response = soc.recv(4096).decode()  # Receive response from server
        print(f"Main server response: {response}")

        # Check if response is valid
        if ":" in response:
            sender_ip, sender_port = response.split(":")
            return sender_ip, int(sender_port)
        elif "Invalid OTP" in response:
            print("OTP is invalid. Please try again.")
        else:
            print("Unexpected response format from server.")
        return None, None
    except Exception as e:
        print(f"Error querying main server: {e}")
        return None, None

def receive_file_from_sender(sender_ip, sender_port):
    """Connects to the sender and receives the encrypted file."""
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_address = (sender_ip, sender_port)
        soc.connect(sender_address)
        print(f"Connected to sender at {sender_ip}:{sender_port}")
        fl=soc.recv(1024).decode().split(",")
        print(fl)
        fn,fs=fl[0][1:-1],fl[1]
        print(f"{fn},{fs}")
        # Receive the encrypted file
        done=False
        flbytes=b""
        with open(fn, "wb") as file:
            progress=tqdm.tqdm(unit='B',unit_scale=True,unit_divisor=1000,total=int(fs))
            while True:
                data = soc.recv(1024).decode()
                print(data+"\n\n")
                if data[-5:] == b"<END>":
                    done=True
                    data=data[:-5]
                # if not data:
                #     break
                file.write(data)
                progress.update(1024)
        user = input("Enter the sender's username: ")
        print(f"Encrypted file received and saved as: {fn}")
        decrypt_file(user,fn,fn)
        soc.close()
    except Exception as e:
        print(f"Error receiving file from sender: {e}")
        raise

def main():
    otp = input("Enter the OTP provided by the sender: ")
    sender_ip, sender_port = query_main_server_for_sender(otp)
    if sender_ip and sender_port:
        # Receive the file
        receive_file_from_sender(sender_ip, sender_port)
        # decrypt_file(user, encrypted_file, output_file)
    else:
        print("Failed to retrieve sender information. Check the OTP or try again.")

if __name__ == "__main__":
    main()
