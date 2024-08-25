#! /bin/python3

## Project_1
## Vivek Vardhan Reddy Yannam - VY22

import socket
import select
import sys

# Check for correct command-line arguments
if len(sys.argv) != 3:
    print("Usage: chatclient <servhost> <servport>")
    sys.exit(1)

# Parse command-line arguments
server_host = sys.argv[1]
server_port = int(sys.argv[2])

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((server_host, server_port))
    print("Connected to", server_host, ":", server_port)

    while True:
        # Use select to monitor sockets
        sockets_list = [sys.stdin, client_socket]
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            if sock == client_socket:
                # recieve message from the server
                message = sock.recv(4096).decode()
                if not message:
                    pass
                # if message is exit signal
                if message.strip() == "-1exit":
                    print("Server Diconnected .... ")
                    client_socket.close()
                    sys.exit(0)
                else:
                    print(message.strip())
            else:
                # User input from the keyboard
                user_msg = sys.stdin.readline()
                client_socket.send(user_msg.encode())
                if user_msg.strip() == "exit" :
                    print("Disconnecting from server ... ")
                    client_socket.close()
                    sys.exit(0)
                # client_socket.send(user_msg.encode())

except KeyboardInterrupt:
    print("\nSomething went wrong ....\nKeyBoard Interrupt ....")
    print("Client terminated.")
    client_socket.send("exit".encode("utf-8"))
    client_socket.close()
    sys.exit(0)
except :
    print("\nSomething went wrong ....")
    print("Client terminated.")
    # client_socket.send("exit".encode("utf-8"))
    client_socket.close()
    sys.exit(0)
