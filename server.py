import socket
import threading
import pickle
from rsa_utils import generate_rsa_keys, decrypt_message
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

clients = {}
public_keys = {}

public_key, private_key = generate_rsa_keys()

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                cipher_rsa = pow(message, public_keys[client][1], public_keys[client][0])
                client.send(cipher_rsa.to_bytes((cipher_rsa.bit_length() + 7) // 8, byteorder='big'))
                print(Fore.GREEN + f"Sent message to client {clients[client]}")
            except Exception as e:
                print(Fore.RED + f"Error sending message to client {clients[client]}: {e}")
                client.close()
                clients.pop(client)

def handle_client(client_socket, address):
    try:
        print(Fore.BLUE + f"Handling client {address}")
        public_key_client = pickle.loads(client_socket.recv(1024))
        public_keys[client_socket] = public_key_client
        print(Fore.YELLOW + f"Received public key from client {address}")

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(Fore.RED + f"Client {address} disconnected.")
                break

            # Вывод зашифрованного сообщения (в байтовом формате) перед расшифровкой
            print(Fore.MAGENTA + f"Encrypted message (bytes) from {address}: {encrypted_message}")

            try:
                encrypted_message_int = int.from_bytes(encrypted_message, byteorder='big')
                message = decrypt_message(encrypted_message_int, private_key)
                print(Fore.CYAN + f"Decrypted message from {address}: {message}")
                broadcast(int(message.encode('utf-8').hex(), 16), client_socket)
            except Exception as e:
                # Если расшифровка не удалась
                print(Fore.RED + f"Error decrypting message from {address}: {e}")
                print(Fore.MAGENTA + f"Encrypted message (bytes): {encrypted_message}")
    except Exception as e:
        print(Fore.RED + f"Error handling client {address}: {e}")
    finally:
        print(Fore.RED + f"Closing connection with client {address}")
        client_socket.close()
        clients.pop(client_socket)
        public_keys.pop(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', 5555))
        server.listen()
        print(Fore.GREEN + "Server started successfully and listening on port 5555...")
    except Exception as e:
        print(Fore.RED + f"Failed to start the server: {e}")
        return

    while True:
        client_socket, address = server.accept()
        print(Fore.BLUE + f"Client connected from {address}")
        clients[client_socket] = address

        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()

if __name__ == "__main__":
    start_server()
