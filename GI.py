import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import pickle
from rsa_utils import generate_rsa_keys, encrypt_message, decrypt_message

client_public_key, client_private_key = generate_rsa_keys()
server_public_key = None

root = tk.Tk()
root.title("RSA Chat Client")

chat_log = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20, wrap='word')
chat_log.grid(row=0, column=0, padx=10, pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.grid(row=1, column=0, padx=10, pady=10)

send_button = tk.Button(root, text="Send", width=10)
send_button.grid(row=1, column=1, padx=10, pady=10)

def add_message(message):
    chat_log.config(state='normal')
    chat_log.insert(tk.END, message + '\n')
    chat_log.config(state='disabled')

def receive_messages(client):
    while True:
        try:
            encrypted_response = client.recv(1024)
            if encrypted_response:
                encrypted_response = int.from_bytes(encrypted_response, byteorder='big')
                decrypted_message = decrypt_message(encrypted_response, client_private_key)
                add_message(f"New message: {decrypted_message}")
            else:
                add_message("Disconnected from server.")
                break
        except Exception as e:
            add_message(f"Error receiving message: {e}")
            client.close()
            break

def send_message():
    message = message_entry.get()
    if message:
        try:
            encrypted_message = encrypt_message(message, server_public_key)
            client.send(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, byteorder='big'))
            add_message(f"Me: {message}")
            message_entry.delete(0, tk.END)
        except Exception as e:
            add_message(f"Error sending message: {e}")

send_button.config(command=send_message)

def start_client():
    global client, server_public_key
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5555))
        client.send(pickle.dumps(client_public_key))
        add_message("Sent public key to server.")

        server_public_key = pickle.loads(client.recv(1024))
        add_message("Received server public key.")

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()
    except Exception as e:
        add_message(f"Failed to connect to the server: {e}")

client_thread = threading.Thread(target=start_client)
client_thread.start()

root.mainloop()
