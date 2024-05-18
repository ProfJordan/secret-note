
# Secret Note

## Description 

**Secret Note** is a web application designed to create secure, self-destructive notes that automatically erase after being read. It's perfect for sending sensitive information that you don't want to remain accessible indefinitely.

![secret note logo](/static/secret-note-logo.png)

## Features

- **Self-Destructive Notes:** Each note is destroyed immediately after it is read, ensuring your sensitive information doesn't stay online longer than necessary.
- **Encryption:** Customizable encryption settings allow you to set a unique salt for each note, enhancing security.
- **Ease of Use:** A simple interface for quickly creating and sharing secure notes.

## Use Cases

Sending secret notes can be incredibly useful in various contexts where privacy and confidentiality are paramount. Here are some practical use cases for utilizing an application like *Secret Note*:

1. **Sensitive Personal Information**

   - Sharing sensitive personal details such as passwords, PINs, or access codes with family members or trusted individuals.

   - Communicating personal or sensitive stories or experiences in support groups online without leaving a digital trail.

2. **Business and Corporate Environments**

   - Sending confidential business information such as contract details, negotiation points, or strategic plans between stakeholders or within departments without risking information leaks.
  
   - Human resources departments sharing sensitive employee information or disciplinary actions in a way that ensures the information can’t be retrieved once read.

3. **Journalism and Whistleblowing**
   
   - Journalists receiving sensitive information from anonymous sources that should not be retrievable after being read to protect the source’s identity and the content’s confidentiality.
     
   - Whistleblowers sharing classified or critical information about illegal activities or misconduct within organizations while maintaining anonymity.

4. **Legal Communications**

   - Attorneys exchanging sensitive information with clients or other legal parties where confidentiality needs to be maintained without leaving an accessible record after the information has been communicated.

   - ~~Law enforcement agencies sharing sensitive information with other agencies or departments while ensuring the information cannot be retrieved once it has been viewed.~~

5. **Technology and Security**
   
   - IT personnel sharing temporary access credentials or recovery keys in situations where such information should not be stored or accessible beyond its immediate use.

   - Conducting secure transactions or communications where data integrity and confidentiality need to be guaranteed.

6. **Personal Relationships**
   
   - Sharing surprise details or sensitive personal messages that the sender wishes to keep private and ensure they are not shared or stored.
     
   - Communicating in environments or situations where privacy is a concern and users need assurances that messages won’t be retained.

7. **Healthcare**

   - Doctors or healthcare providers sending health-related information to patients or other medical staff in a manner compliant with privacy regulations, ensuring the information isn’t accessible after it’s been read.
     
   - Medical professionals sharing sensitive information with patients or other medical staff in a way that ensures the information cannot be retrieved once it has been viewed.

8. **Emergency Communication**

   - Transmitting codes, coordinates, or sensitive instructions in emergency or security-related scenarios where information must not fall into the wrong hands after initial use.

9. **Activism and Security Culture**
    
    - Activists sharing sensitive information or instructions with other activists or members of their organization in a way that ensures the information cannot be retrieved once it has been viewed.

10. **Government and Political Organizations**
    
    - Sending sensitive information to political or government officials in a way that ensures the information is not accessible after it’s been read.

Applications like *Secret Note* provide a secure channel for these types of communications, reducing the risk of information leaks and ensuring messages are destroyed after they serve their purpose. This makes them invaluable in any situation where information confidentiality is critical.

## Installation

To set up the *Secret Note* app on your local machine, follow these steps:


1. Clone the repository to your local machine:
`git clone https://github.com/ProfJordan/secret-note.git`

2. Install dependencies:
`pip install -r requirements.txt`

3. Initialize the database:
`python db-setup.py`

4. Start the application:
`flask run`

## Usage

To use *Secret Note*, simply visit the main page, enter your message, and optionally provide a custom salt for encryption. Submitting the form will generate a link to the encrypted note. Share this link with your intended recipient — remember, the note will self-destruct after it’s read!

## Screenshot

![App Screenshot](/static/secret-note-screenshot.png)

## Tech Stack

**Client:** [HTML](https://html.spec.whatwg.org/), [CSS](https://www.w3.org/TR/CSS/#css), [Bootstrap](https://getbootstrap.com/)

**Server:** [Flask](https://flask.palletsprojects.com/), [Python](https://www.python.org/), [Cryptography](https://github.com/pyca/cryptography)

**Database:** [Sqlite3](https://www.sqlite.org/)

## Technical Stuff

#### Flask
The app uses the [Flask](https://flask.palletsprojects.com/) framework to handle routing and rendering.
 - ##### Main Routes
   - **Create Note**: `'/'`
   -  **Note Link**: `'/note/<note_id>'`

#### Creating a note
When a user creates a note, the message is encrypted and stored in a database along with a unique identifier (ID), in this case the generated salt key.

#### Encryption
The app uses the python [Cryptography](https://github.com/pyca/cryptography) library to encrypt and decrypt messages. The encryption process involves generating a [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) and then using the salt to generate a [key](https://en.wikipedia.org/wiki/Key_(cryptography)) for the encryption. The key is then used to encrypt the message. This allows for robust security with your encrypted secret message. See the functions section below for even more details.

Here's an example of how the encryption works:

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':  # Check if the form has been submitted
            message = request.form['message']  # Get the message from the form
            salt = request.form['salt']  # Get the custom salt from the form for encryption
            if salt == '':
                key = functions.generate_key()  # Generate a random encryption key if no salt is provided
            else:
                key = functions.derive_key(salt)  # Derive an encryption key from the provided salt
            
            encrypted_message = functions.encrypt_message(message, key)  # Encrypt the message using the derived/generated key
            note_id = save_message(encrypted_message, key)  # Save the encrypted message to the database and retrieve its unique ID
            link = url_for('note', note_id=note_id, _external=True)  # Generate a URL for the created note
            return render_template('note_link.html', link=link)  # Display the note link to the user
        return render_template('index.html')  # Show the main page form to create a new note

##### Overview of the Encryption functions:
Inside functions.py you'll find the encryption functions used for encrypting the notes:

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



#### Storing the Note
The app uses the [Sqlite3](https://www.sqlite.org/) database to store the encrypted notes. The database stores the encrypted message, the salt, and the unique ID.

Here's an example of how the note is stored:

    def save_message(encrypted_message, key):
        conn = sqlite3.connect('secret.db')  # Open a connection to the SQLite database
        cursor = conn.cursor()  # Create a cursor object to execute SQL queries
        note_id = uuid.uuid4().hex  # Generate a unique ID for the note using UUID
        cursor.execute('INSERT INTO notes (id, message, salt) VALUES (?, ?, ?)', (note_id, encrypted_message, key)) # Inserts values into Database
        conn.commit()  # Commit the changes to the database
        conn.close()  # Close the database connection
        return note_id  # Return the ID of the newly created note

#### Note Link
As shown above in the main encryption function. The app generates a unique URL link for each note. The link is generated using the [Fernet](https://cryptography.io/en/latest/fernet/) symmetric-key encryption algorithm.

#### Accessing the Note
When a recipient accesses the note using the unique URL link, the application retrieves the note from the database.

Here's an example of how the note is accessed in the database:

    @app.route('/note/<note_id>')
    def note(note_id):
        conn = sqlite3.connect('secret.db')  # Connect to the database
        cursor = conn.cursor()  # Create a cursor to perform database operations
        cursor.execute('SELECT message, salt FROM notes WHERE id = ?', (note_id,))  # Retrieve the message and key for the note
        row = cursor.fetchone()  # Fetch one record from the database

#### Decrypting the Note
Upon retrieval, the application decrypts the note using the stored key, then prepares it for presentation to the viewer.

Here's an example of how the note is then decrypted:

    if row:
                message = functions.decrypt_message(row[0], row[1])  # Decrypt the message using the stored key
                delete_message(note_id)  # Delete the message from the database after it is read
                if message:
                    return render_template('display_note.html', message=message)  # Show the decrypted message to the user
                else:
                    return render_template('display_error.html', error="Salt incorrect or message corrupted.")  # Show an error if decryption fails
            return render_template('display_error.html', error="Note not found or already read and destroyed.")  # Show an error if the note doesn't exist or has been deleted

#### Self-Destruct (Deleting the Note)
Immediately after the note is displayed, a function is triggered to delete the note from the database. This ensures the note cannot be accessed again, adhering to the self-destruct concept. Once the browser window is closed the note is gone forever. If the user then visits the note link again it will be unavailable, as the note was already destroyed.

Here's an example of how the self-destruct function works:


    def delete_message(note_id):
        conn = sqlite3.connect('secret.db')  # Connect to the database
        cursor = conn.cursor()  # Create a cursor to execute SQL commands
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))  # Delete the note from the database
        conn.commit()  # Commit the changes
        conn.close()  # Close the connection to the database


#### Database Management
The app directly interacts with a [Sqlite3](https://www.sqlite.org/) database. The database stores the encrypted message and the salt used to encrypt the message without additional ORM layers.

#### Deployment
When running a [demo of the app](https://secret-note.pinebee.fun/) is currently deployed using [Heroku](https://www.heroku.com/). You can also deploy this app locally or within your own server.

## Contributing

Contributions are welcome! Please feel free to fork the repository, make changes, and submit a pull request. If you have any suggestions or issues, please post them in the issues section of the GitHub repository.

## Author

- [@ProfJordan](https://www.github.com/ProfJordan)

## License

[![Creative Commons Attribution-ShareAlike (CC BY-SA 4.0)](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-sa.png)](https://creativecommons.org/licenses/by-sa/4.0/)

[Creative Commons Attribution-ShareAlike (CC BY-SA 4.0) ](https://creativecommons.org/licenses/by-sa/4.0/)

## Ideas / Roadmap

- [x]   Better message display
- [ ]   Cat memes for errors
- [ ]   Add Password Protection

Password Protection Option would add an additional security layer. The user would need to provide the note link and then enter a password to access it.
