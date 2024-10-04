import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import pickle
from rsa_utils import generate_rsa_keys, encrypt_message, decrypt_message

client_public_key, client_private_key = generate_rsa_keys()
server_public_key = None
dark_mode = True

root = tk.Tk()
root.title("cordRSA")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

def switch_theme():
    if theme_switch_var.get():
        apply_dark_mode()
    else:
        apply_light_mode()

def apply_dark_mode():
    root.configure(bg="#2E2E2E")
    header_frame.configure(bg="#2E2E2E")
    app_label.configure(bg="#2E2E2E", fg="white")
    chat_log.configure(bg="#1C1C1C", fg="white")
    message_entry.configure(bg="#333333", fg="white")
    send_button.configure(bg="#4CAF50", fg="white")
    theme_switch.configure(bg="#2E2E2E", fg="white", selectcolor="#2E2E2E")
    chat_log.tag_config("message_color", foreground="white")

def apply_light_mode():
    root.configure(bg="#F0F0F0")
    header_frame.configure(bg="#F0F0F0")
    app_label.configure(bg="#F0F0F0", fg="black")
    chat_log.configure(bg="white", fg="black")
    message_entry.configure(bg="white", fg="black")
    send_button.configure(bg="#007BFF", fg="white")
    theme_switch.configure(bg="#F0F0F0", fg="black", selectcolor="#F0F0F0")
    chat_log.tag_config("message_color", foreground="black")

header_frame = tk.Frame(root, bg="#2E2E2E")
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

app_label = tk.Label(header_frame, text="cordRSA", font=("Arial", 24), bg="#2E2E2E", fg="white")
app_label.pack(side="left", padx=10, pady=10)

theme_switch_var = tk.BooleanVar(value=True)
theme_switch = tk.Checkbutton(
    header_frame, text="Dark Mode", variable=theme_switch_var, command=switch_theme, 
    bg="#2E2E2E", fg="white", selectcolor="#2E2E2E", font=("Arial", 12)
)
theme_switch.pack(side="right", padx=10, pady=10)

chat_log = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20, wrap='word', bg="#1C1C1C", fg="white", font=("Arial", 12))
chat_log.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

message_entry = tk.Entry(root, width=40, bg="#333333", fg="white", font=("Arial", 12))
message_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

send_button = tk.Button(root, text="Send", width=10, bg="#4CAF50", fg="white", font=("Arial", 12))
send_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

def add_message(sender, message):
    chat_log.config(state='normal')
    if sender == "me":
        chat_log.insert(tk.END, "Me: ", "me_color")
    else:
        chat_log.insert(tk.END, f"{sender}: ", "other_color")
    
    chat_log.insert(tk.END, f"{message}\n", "message_color")
    chat_log.config(state='disabled')
    chat_log.see(tk.END)

chat_log.tag_config("me_color", foreground="#00FF00")
chat_log.tag_config("other_color", foreground="#FF6347")
chat_log.tag_config("message_color", foreground="white")

def receive_messages(client):
    while True:
        try:
            encrypted_response = client.recv(1024)
            if encrypted_response:
                encrypted_response = int.from_bytes(encrypted_response, byteorder='big')
                decrypted_message = decrypt_message(encrypted_response, client_private_key)
                add_message("Other", decrypted_message)
            else:
                add_message("System", "Disconnected from server.")
                break
        except Exception as e:
            add_message("System", f"Error receiving message: {e}")
            client.close()
            break

def send_message():
    message = message_entry.get()
    if message:
        try:
            encrypted_message = encrypt_message(message, server_public_key)
            client.send(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, byteorder='big'))
            add_message("me", message)
            message_entry.delete(0, tk.END)
        except Exception as e:
            add_message("System", f"Error sending message: {e}")

send_button.config(command=send_message)

def start_client():
    global client, server_public_key
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5555))
        client.send(pickle.dumps(client_public_key))
        add_message("System", "Sent public key to server.")

        server_public_key = pickle.loads(client.recv(1024))
        add_message("System", "Received server public key.")

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()
    except Exception as e:
        add_message("System", f"Failed to connect to the server: {e}")

client_thread = threading.Thread(target=start_client)
client_thread.start()

def on_closing():
    if client:
        client.close()
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

apply_dark_mode()
root.mainloop()
