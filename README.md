# RSA-Coded Chat Application

This is a simple client-server chat application that uses RSA encryption for secure communication between clients and the server. The project is written in Python and includes color-coded logging for better readability of messages and errors.

## Features
- **RSA Encryption**: Secure message transmission between clients and server using RSA public and private key pairs.
- **Real-Time Communication**: Multi-threading allows clients to send and receive messages simultaneously.
- **Color-Coded Logging**: Terminal outputs are color-coded using the `colorama` library to easily distinguish between message types and errors.
- **Gitignore Configuration**: Excludes unnecessary files such as `__pycache__` and other auto-generated Python files.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repository.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. (Optional) If `colorama` is not listed in `requirements.txt`, install it manually:
    ```bash
    pip install colorama
    ```

## Usage

1. **Start the server**:
    ```bash
    python server.py
    ```

2. **Start the client** (in a separate terminal or on a different machine):
    ```bash
    python client.py
    ```

## Folder Structure
- `client.py`: The client-side code for sending and receiving encrypted messages.
- `server.py`: The server-side code for handling multiple clients and broadcasting messages.
- `rsa_utils.py`: RSA encryption utilities for generating keys, encrypting, and decrypting messages.
- `.gitignore`: Excludes `__pycache__` and other unnecessary files.

## License
This project is open source and available under the [MIT License](LICENSE).
