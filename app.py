from flask import Flask, render_template, request, redirect, url_for
import functions
import sqlite3
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        password = request.form['password']
        if password == '':
            key = functions.generate_key()
        else:
            key = functions.derive_key(password)
        
        encrypted_message = functions.encrypt_message(message, key)
        note_id = save_message(encrypted_message, key)
        link = url_for('note', note_id=note_id, _external=True)
        return render_template('note_link.html', link=link)
    return render_template('index.html')

def save_message(encrypted_message, key):
    conn = sqlite3.connect('secret.db')
    cursor = conn.cursor()
    note_id = uuid.uuid4().hex  # Generate a unique ID for the note
    cursor.execute('INSERT INTO notes (id, message, password) VALUES (?, ?, ?)',
                   (note_id, encrypted_message, key))
    conn.commit()
    conn.close()
    return note_id

@app.route('/note/<note_id>')
def note(note_id):
    conn = sqlite3.connect('secret.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message, password FROM notes WHERE id = ?', (note_id,))
    row = cursor.fetchone()
    if row:
        message = functions.decrypt_message(row[0], row[1])
        delete_message(note_id)
        if message:
            return message
        else:
            return "Password incorrect or message corrupted."
    return "Note not found or already read & destroyed."


def delete_message(note_id):
    conn = sqlite3.connect('secret.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)
