import socket
import threading
import pickle
from logic.rsa_utils import generate_rsa_keys, encrypt_message, decrypt_message

class ClientLogic:
    def __init__(self, update_ui_callback):
        self.client = None
        self.server_public_key = None
        self.client_public_key, self.client_private_key = generate_rsa_keys()
        self.update_ui_callback = update_ui_callback
        self.in_voice_chat = False

    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 5555))
            self.client.send(pickle.dumps(self.client_public_key))
            self.update_ui_callback("System", "Sent public key to server.")

            self.server_public_key = pickle.loads(self.client.recv(1024))
            self.update_ui_callback("System", "Received server public key.")

            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
        except Exception as e:
            self.update_ui_callback("System", f"Failed to connect to the server: {e}")

    def receive_messages(self):
        while True:
            try:
                encrypted_response = self.client.recv(1024)
                if encrypted_response:
                    encrypted_response = int.from_bytes(encrypted_response, byteorder='big')
                    decrypted_message = decrypt_message(encrypted_response, self.client_private_key)

                    if decrypted_message.startswith("Voice Chat Users:"):
                        users = decrypted_message.replace("Voice Chat Users:", "").strip().split(", ")
                        self.update_ui_callback("update_users", users)  # Передаем обновленный список пользователей
                    else:
                        self.update_ui_callback("Other", decrypted_message)
                else:
                    self.update_ui_callback("System", "Disconnected from server.")
                    break
            except Exception as e:
                self.update_ui_callback("System", f"Error receiving message: {e}")
                self.client.close()
                break


    def send_message(self, message):
        if message:
            try:
                encrypted_message = encrypt_message(message, self.server_public_key)
                self.client.send(encrypted_message.to_bytes((encrypted_message.bit_length() + 7) // 8, byteorder='big'))
                self.update_ui_callback("me", message)
            except Exception as e:
                self.update_ui_callback("System", f"Error sending message: {e}")

    def toggle_voice_chat(self):
        if self.in_voice_chat:
            self.leave_voice_chat()
        else:
            self.enter_voice_chat()

    def enter_voice_chat(self):
        try:
            encrypted_command = encrypt_message("Enter VC", self.server_public_key)
            self.client.send(encrypted_command.to_bytes((encrypted_command.bit_length() + 7) // 8, byteorder='big'))
            self.in_voice_chat = True
            self.update_ui_callback("update_button", "Leave VC")
        except Exception as e:
            self.update_ui_callback("System", f"Error entering voice chat: {e}")

    def leave_voice_chat(self):
        try:
            encrypted_command = encrypt_message("Leave VC", self.server_public_key)
            self.client.send(encrypted_command.to_bytes((encrypted_command.bit_length() + 7) // 8, byteorder='big'))
            self.in_voice_chat = False
            self.update_ui_callback("update_button", "Enter VC")
        except Exception as e:
            self.update_ui_callback("System", f"Error leaving voice chat: {e}")

    def close_connection(self):
        if self.client:
            if self.in_voice_chat:
                self.leave_voice_chat()
            self.client.close()
