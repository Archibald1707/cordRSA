# RSA-Coded Chat Application 🔒

This is a simple client-server chat application that uses RSA encryption for secure communication between clients and the server. The project is written in Python and includes color-coded logging for better readability of messages and errors. A graphical user interface (GUI) client is also available using Tkinter.

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

## ✨ Features
- **RSA Encryption**: Secure message transmission between clients and server using RSA public and private key pairs.
- **Real-Time Communication**: Multi-threading allows clients to send and receive messages simultaneously.
- **Graphical User Interface**: A Tkinter-based GUI client that allows users to send and receive encrypted messages through a simple interface.
- **Cryptographically Secure Random Numbers**: The `secrets` module is used to generate secure random numbers for RSA key generation.
- **Color-Coded Logging**: Terminal outputs are color-coded using the `colorama` library to easily distinguish between message types and errors.
- **Gitignore Configuration**: Excludes unnecessary files such as `__pycache__` and other auto-generated Python files.

## 📥 Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Archibald1707/cordRSA
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. (Optional) If `colorama` is not listed in `requirements.txt`, install it manually:
    ```bash
    pip install colorama
    ```

## 🚀 Usage

1. **Start the server**:
    ```bash
    python server.py
    ```

2. **Start the client** (in a separate terminal or on a different machine):
    ```bash
    python client.py
    ```

## 📂 Folder Structure

```
cordRSA
│   .gitattributes
│   .gitignore
│   client.py
│   LICENSE
│   README.md
│   requirements.txt
│   server.py
│   setup.py
│
├───gui
│   │   interface.py
│   │
│   └───__pycache__
│           interface.cpython-312.pyc
│
├───logic
│   │   client_logic.py
│   │   rsa_utils.py
│   │
│   └───__pycache__
│           client_logic.cpython-312.pyc
│           rsa_utils.cpython-312.pyc
│
└───__pycache__
        rsa_utils.cpython-312.pyc
```

## 🤝 Contribution

Contributions are welcome! If you would like to contribute to the project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## 📜 License
This project is open source and available under the [MIT License](LICENSE).

