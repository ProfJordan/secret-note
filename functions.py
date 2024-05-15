from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from flask import render_template

# def get_fernet_key(password: str):
#     """Generate a Fernet key based on the provided password, ensuring it's treated as a string"""
#     # Fixed salt (should be random and stored securely for production use)
#     salt = b'secret_salt_here'
#     # Use PBKDF2HMAC for key derivation
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     # Make sure the password is a string before encoding
#     password_bytes = password.encode()  # Encode the password to bytes
#     key = urlsafe_b64encode(kdf.derive(password_bytes))  # Correctly derive and encode the key
#     return key

def derive_key(password: str):
    """ Derive a Fernet key from a given password """
    password_bytes = password.encode()  # Convert the password to bytes
    salt = b'some_constant_salt'  # Should be securely chosen in production. Use the same salt throughout.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password_bytes))  # Generate a Fernet-compatible key
    return key

def generate_key():
    """ Generate a key for encryption """
    return Fernet.generate_key()

def encrypt_message(message, key):
    """ Encrypt the message """
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    """ Decrypt the message """
    f = Fernet(key)
    try:
        return f.decrypt(encrypted_message).decode()
    except:
        return None

# def generate_key():
#     """ Generate a key for encryption """
#     return Fernet.generate_key()

# def encrypt_message(message: str, password: str):
#     """Encrypt a message using a password"""
#     key = derive_key(password)
#     f = Fernet(key)
#     return f.encrypt(message.encode()).decode()

# def decrypt_message(token: str, password: str):
#     """Decrypt a message using a password"""
#     key = derive_key(password)
#     f = Fernet(key)
#     try:
#         return f.decrypt(token.encode()).decode()
#     except Exception as e:
#         print("Decryption failed:", e)
#         return None

def cat_message(message, code=400):
    """Render message as a cat meme to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("cat_message.html", top=code, bottom=escape(message)), code