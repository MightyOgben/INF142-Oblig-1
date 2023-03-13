import socket
from colorama import Fore, Style

# Creating a socket to connect to the server
SERVER = "localhost"
PORT = 42694
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# Function to handle the connection to the server
def handle_server():
    while True:
        message = client.recv(1024).decode()  # Receive the message from the server, one of the two below.
        print(f"{message}\n")
        # If the message from the server is "What do you want to know? \n", we ask the user for a question
        if message == "What do you want to know?\n":
            question = input("> ")  # User inputs a question
            if question == "exit":  # Check if user input is "exit"
                client.sendall(question.encode())  # Send "exit" command to the server
                print("You have disconnected from the server.\n")  # Inform the user that they've disconnected
                break  # Break out of the loop
            client.sendall(question.encode())   # Send the question to the server
            print(f"{Fore.YELLOW}-- Your question has been sent --{Style.RESET_ALL}\n")   # Print a message to the user,
            # informing them that their question has been sent
            answer_in = client.recv(1024).decode()  # Receive the answer from the server
            print(f"{Fore.LIGHTGREEN_EX}Answer:{Style.RESET_ALL} {answer_in}\n")  # Print the answer to the user

        # If the message from the server is "Waiting for a question to answer. \n",
        # we wait for a question from the server
        elif message == "Waiting for a question to answer.\n":
            question = client.recv(1024).decode()  # Receive the question from the server
            print(f"{Fore.LIGHTBLUE_EX}Question:{Style.RESET_ALL} {question}\n")  # Print the question to the user
            answer_out = input("> ")  # User inputs an answer
            if answer_out == "exit":  # Check if user input is "exit"
                client.sendall(answer_out.encode())  # Send "exit" command to the server
                print("You have disconnected from the server.\n")  # Inform the user that they've disconnected
                break  # Break out of the loop
            client.sendall(answer_out.encode())  # Send the answer to the server
            print(f"{Fore.YELLOW}-- Your answer has been sent --{Style.RESET_ALL}\n")  # Inform the advisor that their
            # answer has been sent


# Start handling the connection to the server
handle_server()
