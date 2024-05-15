from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from flask import render_template

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