from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)

users = {}  # Store user credentials
notes = {}  # Store notes for each user separately

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('notes_page'))
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        if username in users:
            return "User already exists. Try logging in.", 400

        users[username] = password
        notes[username] = []  # Initialize empty notes for user
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and bcrypt.check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('notes_page'))
        
        return "Invalid credentials", 403

    return render_template('login.html')

@app.route('/notes')
def notes_page():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_notes = notes.get(session['user'], [])
    return render_template('notes.html', notes=user_notes)

@app.route('/get_notes')
def get_notes():
    if 'user' in session:
        return jsonify({"notes": notes.get(session['user'], [])})
    return jsonify({"error": "Unauthorized"}), 403

@app.route('/save', methods=['POST'])
def save_note():
    if 'user' in session:
        note = request.json.get("note")
        if note:
            notes[session['user']].append(note)
            return jsonify({"message": "Note saved!", "notes": notes[session['user']]})
        return jsonify({"error": "No Note Provided"}), 400

    return jsonify({"error": "Unauthorized"}), 403

@app.route('/update/<int:note_index>', methods=['PUT'])
def update_note(note_index):
    if 'user' in session:
        new_note = request.json.get("note")
        if new_note and 0 <= note_index < len(notes[session['user']]):
            notes[session['user']][note_index] = new_note
            return jsonify({"message": "Note updated!"})
        return jsonify({"error": "Invalid Note Index"}), 400

    return jsonify({"error": "Unauthorized"}), 403

@app.route('/delete/<int:note_index>', methods=['DELETE'])
def delete_note(note_index):
    if 'user' in session:
        if 0 <= note_index < len(notes[session['user']]):
            notes[session['user']].pop(note_index)
            return jsonify({"message": "Note deleted!"})
        return jsonify({"error": "Invalid Note Index"}), 400

    return jsonify({"error": "Unauthorized"}), 403

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
