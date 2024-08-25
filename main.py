import sender
import receiver
import sender.sender_main
import server

def main():
    print("Welcome to Secure File Transfer!")
    print("1. Send a file")
    print("2. Receive a file")
    # print("3. Start a server")
    choice = input("Enter your choice: ")
    if choice == "1":
        sender.sender_main.main()
    elif choice == "2":
        receiver.main()
    # elif choice == "3":
    #     server.main()
    else:
        print("Invalid choice. Exiting...")
        exit(1)

if __name__ == "__main__":
    main()