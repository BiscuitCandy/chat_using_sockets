#! /bin/python3

## Project_1
## Author: Vivek Vardhan Reddy Yannam - VY22

import socket
import select
import random
import signal
import sys

# Define constants
SERVER_HOST = 'localhost'
SERVER_PORT = 0
BUFFER_SIZE = 1024

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen new client connections
server_socket.listen(15)
print("Server is listening on", server_socket.getsockname()[0], ":", server_socket.getsockname()[1])

# Create a list of connected clients
connected_clients = []

# broadcast the message
def broadcast(message, sender_socket):
    for client_socket in connected_clients:
        # Send the message to all clients except the sender
        if client_socket != server_socket and client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                # Remove the client if an issue while sending data
                client_socket.close()
                connected_clients.remove(client_socket)

def sigint_handler(signum, frame):

    print("Server is disconnected")
    broadcast("-1exit".encode("utf-8"), None)
    for client in connected_clients:
        client.close()
    server_socket.close()
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, sigint_handler)

while True:
    # Use select to monitor sockets for incoming data
    read_sockets, a, b = select.select([server_socket] + connected_clients, [], [])

    for sock in read_sockets:
        if sock == server_socket:
            # A new client is trying to connect
            client_socket, client_address = server_socket.accept()
            connected_clients.append(client_socket)
            print("Client connected")

            # Send a welcome message to the new client
            client_socket.send("Welcome to the chat server!".encode("utf-8"))

        else:
            # There is data to be read from an existing client
            try:
                data = sock.recv(BUFFER_SIZE)
                
                # if client sent "exit" disconnect the client
                if data.decode("utf-8").strip() == "exit" :
                    print("A client disconnected")
                    sock.close()
                    connected_clients.remove(sock)

                # else a message then broadcast
                elif data:
                    message = data.decode("utf-8").strip()
                    print("Received a message:", message)
                    broadcast(data, sock)
                else:
                    # Remove the client if it's no longer sending data
                    sock.close()
                    connected_clients.remove(sock)
            except Exception as e:
                print("Error:", str(e))
                sock.close()
                connected_clients.remove(sock)

# Close the server socket when finished
server_socket.close()
