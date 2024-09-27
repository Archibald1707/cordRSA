import socket
import threading
import pickle
from rsa_utils import generate_rsa_keys, encrypt_message, decrypt_message
from colorama import init, Fore, Style

init(autoreset=True)

public_key, private_key = generate_rsa_keys()

def receive_messages(client):
    while True:
        try:
            encrypted_response = client.recv(1024)
            if encrypted_response:
                print(Fore.MAGENTA + f"\nEncrypted message (bytes): {encrypted_response}")
                
                encrypted_response = int.from_bytes(encrypted_response, byteorder='big')
                decrypted_message = decrypt_message(encrypted_response, private_key)
                print(Fore.CYAN + f"\nNew message: {decrypted_message}")
            else:
                print(Fore.YELLOW + "Disconnected from server.")
                break
        except Exception as e:
            print(Fore.RED + f"Error receiving message: {e}")
            client.close()
            break

def send_messages(client):
    while True:
        try:
            message = input("Enter message: ").encode('utf-8')
            encrypted_message = encrypt_message(message.decode('utf-8'), public_key)
            client.send(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, byteorder='big'))
            print(Fore.GREEN + "Message sent successfully.")
        except Exception as e:
            print(Fore.RED + f"Error sending message: {e}")
            client.close()
            break

def start_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))

        client.send(pickle.dumps(public_key))

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
