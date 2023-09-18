import socket
import threading
import pickle
import game

# Constants
SERVER_IP = 'localhost'
SERVER_PORT = 3000
BUFFER_SIZE = 1024

# Initialize the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER_IP, SERVER_PORT)
server_socket.bind(server_address)
server_socket.listen(5)
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

# List to store connected client threads
client_threads = []
connected_clients = []

# Function to handle a single client connection
def handle_client(client_socket: socket.socket):
  print("Handle client")
  while True:
    try:
      receive_data = client_socket.recv(BUFFER_SIZE)
    except ConnectionResetError:
        break
    if not receive_data:
      break
    data = pickle.loads(receive_data)
    game.update(connected_clients,client_socket,data)
  #   # Send game results to client(s)
  print(client_socket.getpeername()[1], " had disconnected")
  connected_clients.remove(client_socket)
  client_socket.close()

# Main server loop
while True:
  client_socket, client_address = server_socket.accept()
  connected_clients.append(client_socket)
  print(f"Connection established with {client_address}")
  game.init(connected_clients,client_socket)
  # Create a new thread for each client
  client_thread = threading.Thread(target=handle_client,
                                   args=(client_socket, ))
  client_thread.start()
  client_threads.append(client_thread)
