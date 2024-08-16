import sqlite3

def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            favorite_genre TEXT
        )
    ''')
    conn.commit()
    conn.close()

def update_user_genre(user_id, new_genre):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET favorite_genre = ? WHERE id = ?', (new_genre, user_id))
    conn.commit()
    conn.close()

def add_user(username, password, favorite_genre):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, favorite_genre) VALUES (?, ?, ?)', (username, password, favorite_genre))
    conn.commit()
    conn.close()

def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user
