import socket
import threading
from colorama import Fore, Back, Style

# Creating the socket and binding it to the port
SERVER = "localhost"
PORT = 42694
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Defining the roles and lists for the server
ROLES = ["advisee", "advisor"]
advisors = []
advisees = []
pairing = {}
busy_advisors = []
role_index = 1


# Function to handle the connection of a client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # A probably horrible way to assign roles, but I wanted them to be one after another.
    global role_index
    # Since we always need an advisee, we first assign that role
    if not advisees:
        role = "advisee"
    # If there is an advisee, we assign the other role, and then switch the index
    else:
        role = ROLES[role_index]
        role_index = (role_index + 1) % len(ROLES)

    # Sending a message to the client, informing them of their roles
    conn.sendall(f"Your role is {Fore.YELLOW}--{role}--{Style.RESET_ALL}".encode())

    # If the client is an advisor, we add them to the advisor list
    if role == "advisor":
        advisors.append(conn)
        print(f"[ADVISOR] {addr} is now an advisor.")
        conn.sendall("Waiting for a question to answer.\n".encode())

    # If the client is an advisee, we add them to the advisee list
    elif role == "advisee":
        advisees.append(conn)
        print(f"[ADVISEE] {addr} is now an advisee.")
        conn.sendall("What do you want to know?\n".encode())

    # Handle the connection and messages of the client
    while True:
        message = conn.recv(1024).decode()
        if message == "exit":
            # If the client disconnects, we remove them from the lists
            if role == "advisee":
                advisees.remove(conn)
                print(f"[DISCONNECT] {addr} disconnected.")
            elif role == "advisor":
                advisors.remove(conn)
                print(f"[DISCONNECT] {addr} disconnected.")
            break

        # If the client is an advisee, we add their question to the questions dictionary
        if role == "advisee":
            print(f"[QUESTION] {addr} asked: {message}")

            # Send the question to an available advisor
            for advisor_conn in advisors:
                if advisor_conn not in busy_advisors:
                    busy_advisors.append(advisor_conn)
                    advisor_conn.sendall(message.encode())
                    pairing[advisor_conn] = conn
                    break

        # If the client is an advisor, we check if they have a question to answer
        elif role == "advisor":

            # Send the answer to the advisee
            advisee_conn = pairing[conn]
            answer = message
            print(f"[ANSWER] {addr} answered: {answer}")
            advisee_conn.sendall(answer.encode())
            advisee_conn.sendall("What do you want to know?\n".encode())
            del pairing[conn]
            busy_advisors.remove(conn)
            conn.sendall("Waiting for a question to answer.\n".encode())


# Function to start the server
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Start the server + apparently needed for debugging :o
if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
