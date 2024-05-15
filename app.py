from flask import Flask, render_template, request, redirect, url_for
import functions
import sqlite3
import uuid

app = Flask(__name__)  # Initialize the Flask application

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

def save_message(encrypted_message, key):
    conn = sqlite3.connect('secret.db')  # Open a connection to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL queries
    note_id = uuid.uuid4().hex  # Generate a unique ID for the note using UUID
    cursor.execute('INSERT INTO notes (id, message, salt) VALUES (?, ?, ?)', (note_id, encrypted_message, key)) # Inserts values into Database
    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection
    return note_id  # Return the ID of the newly created note

@app.route('/note/<note_id>')
def note(note_id):
    conn = sqlite3.connect('secret.db')  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to perform database operations
    cursor.execute('SELECT message, salt FROM notes WHERE id = ?', (note_id,))  # Retrieve the message and key for the note
    row = cursor.fetchone()  # Fetch one record from the database
    if row:
        message = functions.decrypt_message(row[0], row[1])  # Decrypt the message using the stored key
        delete_message(note_id)  # Delete the message from the database after it is read
        if message:
            return render_template('display_note.html', message=message)  # Show the decrypted message to the user
        else:
            return render_template('display_error.html', error="Salt incorrect or message corrupted.")  # Show an error if decryption fails
    return render_template('display_error.html', error="Note not found or already read and destroyed.")  # Show an error if the note doesn't exist or has been deleted

def delete_message(note_id):
    conn = sqlite3.connect('secret.db')  # Connect to the database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))  # Delete the note from the database
    conn.commit()  # Commit the changes
    conn.close()  # Close the connection to the database

if __name__ == '__main__':
    app.run(debug=True)  # Run the application with debug mode enabled
