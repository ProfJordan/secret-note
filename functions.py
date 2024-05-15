from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from flask import render_template

def derive_key(password: str):
    """ Derive a Fernet key from a given password.
    
    Args:
        password (str): The password from which the key is derived.
        
    Returns:
        bytes: The derived key that can be used for encryption.
        
    Notes:
        The salt used in this function should be securely chosen and kept constant across the application.
    """
    password_bytes = password.encode()  # Convert the password to bytes
    salt = b'some_constant_salt'  # Should be securely chosen and stored safely in production
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Use SHA256 hashing algorithm
        length=32,  # Desired length of the derived key in bytes
        salt=salt,  # Salt added for cryptographic strength
        iterations=100000,  # Number of iterations to run the algorithm (making it harder to crack)
        backend=default_backend()  # Cryptographic backend used
    )
    key = urlsafe_b64encode(kdf.derive(password_bytes))  # Generate a URL-safe, Fernet-compatible key
    return key

def generate_key():
    """ Generate a random key for Fernet encryption.
    
    Returns:
        bytes: A securely generated random encryption key.
    """
    return Fernet.generate_key()  # Generate a random encryption key

def encrypt_message(message, key):
    """ Encrypt a message using Fernet encryption.
    
    Args:
        message (str): The plaintext message to encrypt.
        key (bytes): The encryption key.
        
    Returns:
        bytes: The encrypted message.
    """
    f = Fernet(key)  # Create a Fernet cipher instance with the provided key
    return f.encrypt(message.encode())  # Encrypt the message and return the encrypted data

def decrypt_message(encrypted_message, key):
    """ Decrypt a message using Fernet encryption.
    
    Args:
        encrypted_message (bytes): The encrypted message to decrypt.
        key (bytes): The encryption key.
        
    Returns:
        str: The decrypted message, or None if decryption fails.
    """
    f = Fernet(key)  # Create a Fernet cipher instance with the provided key
    try:
        return f.decrypt(encrypted_message).decode()  # Attempt to decrypt and decode the message
    except:
        return None  # Return None if decryption fails
