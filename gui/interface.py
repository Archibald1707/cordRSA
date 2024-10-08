import tkinter as tk
from tkinter import scrolledtext
from logic.client_logic import ClientLogic

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.client_logic = ClientLogic(self.add_message)

        self.build_interface()
        self.client_logic.start_client()
        self.apply_dark_mode()

    def update_voice_chat_users(self, users):
        self.user_list.delete(0, tk.END)
        for user in users:
            self.user_list.insert(tk.END, user)

    def build_interface(self):
        self.root.title("cordRSA")
        self.root.geometry("800x600")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.app_label = tk.Label(self.header_frame, text="cordRSA", font=("Arial", 24))
        self.app_label.pack(side="left", padx=10, pady=10)

        self.theme_switch_var = tk.BooleanVar(value=True)
        self.theme_switch = tk.Checkbutton(self.header_frame, text="Dark Mode", variable=self.theme_switch_var, command=self.switch_theme)
        self.theme_switch.pack(side="right", padx=10, pady=10)

        self.left_frame = tk.Frame(self.root, width=200)
        self.left_frame.grid(row=1, column=0, sticky="nswe")

        self.users_label = tk.Label(self.left_frame, text="Voice Chat Users", font=("Arial", 12))
        self.users_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.user_list = tk.Listbox(self.left_frame, font=("Arial", 10))
        self.user_list.grid(row=1, column=0, padx=5, pady=5, sticky="nswe")

        self.enter_vc_button = tk.Button(self.left_frame, text="Enter VC", command=self.client_logic.toggle_voice_chat)
        self.enter_vc_button.grid(row=2, column=0, padx=5, pady=5, sticky="we")

        self.chat_log = scrolledtext.ScrolledText(self.root, state='disabled', wrap='word', font=("Arial", 12))
        self.chat_log.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.message_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.message_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=1, sticky="e")

    def add_message(self, sender, message):
        if sender == "update_users":
            self.update_voice_chat_users(message)
        elif sender == "update_button":
            self.enter_vc_button.config(text=message)
        else:
            self.chat_log.config(state='normal')
            self.chat_log.insert(tk.END, f"{sender}: {message}\n")
            self.chat_log.config(state='disabled')
            self.chat_log.see(tk.END)

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.client_logic.send_message(message)

    def switch_theme(self):
        if self.theme_switch_var.get():
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def apply_dark_mode(self):
        self.root.configure(bg="#2E2E2E")
        self.header_frame.configure(bg="#2E2E2E")
        self.app_label.configure(bg="#2E2E2E", fg="white")
        self.chat_log.configure(bg="#1C1C1C", fg="white")
        self.message_entry.configure(bg="#333333", fg="white")
        self.send_button.configure(bg="#4CAF50", fg="white")
        self.theme_switch.configure(bg="#2E2E2E", fg="white", selectcolor="#2E2E2E")
        self.left_frame.configure(bg="#2E2E2E")
        self.users_label.configure(bg="#2E2E2E", fg="white")
        self.user_list.configure(bg="#1C1C1C", fg="white")
        self.enter_vc_button.configure(bg="#4CAF50", fg="white")

    def apply_light_mode(self):
        self.root.configure(bg="#F0F0F0")
        self.header_frame.configure(bg="#F0F0F0")
        self.app_label.configure(bg="#F0F0F0", fg="black")
        self.chat_log.configure(bg="white", fg="black")
        self.message_entry.configure(bg="white", fg="black")
        self.send_button.configure(bg="#007BFF", fg="white")
        self.theme_switch.configure(bg="#F0F0F0", fg="black", selectcolor="#F0F0F0")
        self.left_frame.configure(bg="#F0F0F0")
        self.users_label.configure(bg="#F0F0F0", fg="black")
        self.user_list.configure(bg="white", fg="black")
        self.enter_vc_button.configure(bg="#007BFF", fg="white")

    def on_closing(self):
        self.client_logic.close_connection()
        self.root.quit()
        self.root.destroy()
