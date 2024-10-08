import socket
import threading
import pickle
from logic.rsa_utils import generate_rsa_keys, decrypt_message, encrypt_message
from colorama import init, Fore

init(autoreset=True)

clients = {}
public_keys = {}
voice_chat_users = set()  # Храним пользователей, которые находятся в голосовом чате

server_public_key, server_private_key = generate_rsa_keys()

def broadcast(message, sender_client):
    sender_address = clients[sender_client]
    for client in clients:
        if client != sender_client:
            try:
                client_public_key = public_keys[client]
                encrypted_message = encrypt_message(f"Message from {sender_address}: {message}", client_public_key)
                client.send(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, byteorder='big'))
                print(Fore.GREEN + f"Sent encrypted message to client {clients[client]}")
            except Exception as e:
                print(Fore.RED + f"Error sending message to client {clients[client]}: {e}")
                client.close()
                clients.pop(client)

def update_voice_chat_users():
    for client in clients:
        try:
            client_public_key = public_keys[client]
            user_list_message = f"Voice Chat Users: {', '.join(voice_chat_users)}"
            encrypted_user_list = encrypt_message(user_list_message, client_public_key)
            client.send(encrypted_user_list.to_bytes((encrypted_user_list.bit_length() + 7) // 8, byteorder='big'))
            print(Fore.GREEN + "Sent updated voice chat user list to clients")
        except Exception as e:
            print(Fore.RED + f"Error sending user list to client {clients[client]}: {e}")

def handle_client(client_socket, address):
    try:
        print(Fore.BLUE + f"Handling client {address}")
        public_key_client = pickle.loads(client_socket.recv(1024))
        public_keys[client_socket] = public_key_client
        print(Fore.YELLOW + f"Received public key from client {address}: {public_key_client}")
        client_socket.send(pickle.dumps(server_public_key))
        print(Fore.YELLOW + f"Sent server public key to client {address}")

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(Fore.RED + f"Client {address} disconnected.")
                break

            print(Fore.MAGENTA + f"Encrypted message (bytes) from {address}: {encrypted_message}")
            encrypted_message_int = int.from_bytes(encrypted_message, byteorder='big')
            decrypted_message = decrypt_message(encrypted_message_int, server_private_key)

            if decrypted_message == "Enter VC":
                voice_chat_users.add(str(address))
                update_voice_chat_users()
            elif decrypted_message == "Leave VC":
                voice_chat_users.discard(str(address))
                update_voice_chat_users()
            else:
                print(Fore.CYAN + f"Decrypted message from {address}: {decrypted_message}")
                broadcast(decrypted_message, client_socket)
    except Exception as e:
        print(Fore.RED + f"Error handling client {address}: {e}")
    finally:
        print(Fore.RED + f"Closing connection with client {address}")
        client_socket.close()
        clients.pop(client_socket)
        public_keys.pop(client_socket)
        voice_chat_users.discard(str(address))
        update_voice_chat_users()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', 5555))
        server.listen()
        print(Fore.GREEN + "Server started successfully and listening on port 5555...")

        while True:
            try:
                client_socket, address = server.accept()
                print(Fore.BLUE + f"Client connected from {address}")
                clients[client_socket] = address

                thread = threading.Thread(target=handle_client, args=(client_socket, address))
                thread.start()
            except KeyboardInterrupt:
                print(Fore.RED + "\nShutting down server...")
                for client in clients:
                    client.close()
                server.close()
                break
    except Exception as e:
        print(Fore.RED + f"Failed to start the server: {e}")

if __name__ == "__main__":
    start_server()
