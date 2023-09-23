import socket
import threading
import pickle

def receive_data_from_server(client_socket,messages):
    try:
        while True:
            # Receive data from the server
            try:
                message_length_bytes = client_socket.recv(4)
                message_length = int.from_bytes(message_length_bytes, byteorder='big')
                message_data = b""
                while len(message_data) < message_length:
                    remaining_bytes = message_length - len(message_data)
                    message_chunk = client_socket.recv(remaining_bytes)
                    if message_chunk :
                        deserialize_data = pickle.loads(message_chunk)
                        messages.put(deserialize_data)
                    message_data += message_chunk
            except socket.error:
                continue

    except Exception as e:
        print(f"Error: {str(e)}")

def connect(server,port,messages):
    # Network
    SERVER_IP = f'{server}.tcp.ngrok.io' if server != 'x' else 'localhost'
    SERVER_PORT = port

    server_address = (SERVER_IP, SERVER_PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    client_socket.setblocking(0)

    # Start a separate thread for receiving data from the server
    receive_thread = threading.Thread(target=lambda:receive_data_from_server(client_socket,messages))
    receive_thread.daemon = True
    receive_thread.start()

    return client_socket

def send_data_to_server(client_socket,data):
    try:
        dumped = pickle.dumps(data)
        message_length = len(dumped).to_bytes(4, byteorder='big')  # 4 bytes for message length
        final_message = message_length + dumped
        client_socket.send(final_message)
    except Exception as e:
        print(f"Error: {str(e)}")