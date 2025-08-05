from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            year TEXT,
            experience TEXT,
            reason TEXT,
            club TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club TEXT,
            event_name TEXT,
            room_no TEXT,
            date TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "✅ Backend is running"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    year = data.get('year')
    experience = data.get('experience')
    reason = data.get('reason')
    club = data.get('club')

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO registrations (name, year, experience, reason, club) VALUES (?, ?, ?, ?, ?)',
                  (name, year, experience, reason, club))
        conn.commit()
        conn.close()
        print("✅ Registration saved:", data)
        return jsonify({'message': 'Registration successful!'}), 200
    except Exception as e:
        print("❌ Error saving registration:", e)
        return jsonify({'message': 'Error saving registration'}), 500

@app.route('/create-event', methods=['POST'])
def create_event():
    data = request.get_json()
    club = data.get('club')
    event_name = data.get('event_name')
    room_no = data.get('room_no')
    date = data.get('date')
    time = data.get('time')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (club, event_name, room_no, date, time) VALUES (?, ?, ?, ?, ?)',
              (club, event_name, room_no, date, time))
    conn.commit()
    conn.close()

    print("✅ Event added:", data)
    return jsonify({'message': 'Event added successfully!'})

@app.route('/registrations', methods=['GET'])
def get_registrations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT name, year, club FROM registrations')
    rows = c.fetchall()
    conn.close()

    registrations = [{'name': row[0], 'year': row[1], 'club': row[2]} for row in rows]
    return jsonify({'registrations': registrations})

@app.route('/events', methods=['GET'])
def get_events():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT club, event_name, room_no, date, time FROM events')
    rows = c.fetchall()
    conn.close()

    events = [{'club': row[0], 'event_name': row[1], 'room_no': row[2], 'date': row[3], 'time': row[4]} for row in rows]
    return jsonify({'events': events})


# Start the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
