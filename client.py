import socket
import threading
import pickle
from rsa_utils import generate_rsa_keys, encrypt_message, decrypt_message
from colorama import init, Fore, Style

init(autoreset=True)

client_public_key, client_private_key = generate_rsa_keys()
server_public_key = None

def receive_messages(client):
    global server_public_key
    while True:
        try:
            encrypted_response = client.recv(1024)
            if encrypted_response:
                print(Fore.MAGENTA + f"Encrypted message (bytes): {encrypted_response}")
                encrypted_response = int.from_bytes(encrypted_response, byteorder='big')
                decrypted_message = decrypt_message(encrypted_response, client_private_key)
                print(Fore.CYAN + f"\nNew message: {decrypted_message}")
            else:
                print(Fore.YELLOW + "Disconnected from server.")
                break
        except Exception as e:
            print(Fore.RED + f"Error receiving message: {e}")
            client.close()
            break

def send_messages(client):
    global server_public_key
    while True:
        try:
            message = input()
            encrypted_message = encrypt_message(message, server_public_key)
            client.send(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, byteorder='big'))
            print(Fore.GREEN + "Message sent successfully.")
        except Exception as e:
            print(Fore.RED + f"Error sending message: {e}")
            client.close()
            break

def start_client():
    global server_public_key
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        client.send(pickle.dumps(client_public_key))
        print(Fore.YELLOW + f"Sent public key to server")
        server_public_key = pickle.loads(client.recv(1024))
        print(Fore.YELLOW + f"Received server public key: {server_public_key}")

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        send_thread = threading.Thread(target=send_messages, args=(client,))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except Exception as e:
        print(Fore.RED + f"Failed to connect to the server: {e}")

if __name__ == "__main__":
    start_client()
