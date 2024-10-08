import secrets
from sympy import isprime, mod_inverse

def generate_prime(bits):
    while True:
        prime = secrets.randbits(bits)
        if isprime(prime):
            return prime

def generate_rsa_keys(bits=1024):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    print(p, q)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi_n)
    return (n, e), (n, d)

def encrypt_message(message, public_key):
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    return pow(message_int, public_key[1], public_key[0])

def decrypt_message(encrypted_message, private_key):
    message_int = pow(encrypted_message, private_key[1], private_key[0])
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, byteorder='big').decode('utf-8')
