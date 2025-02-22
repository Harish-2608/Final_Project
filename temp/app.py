from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a random secret key

# Database connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="hari",  # Use a new user instead of 'root'
        password="yourpassword",
        database="heritage_guide"
    )
    return conn

# Home page
@app.route('/')
def home():
    return render_template('login.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password and decode it for MySQL storage
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            flash('Username already exists! Please choose a different one.')
        else:
            # Insert new user into the database
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (%s, %s)', (username, password_hash))
            conn.commit()
            flash('Registration successful! Please login.')
            cursor.close()
            conn.close()
            return redirect(url_for('login'))

        cursor.close()
        conn.close()

    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor

        # Fetch the user from the database
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode()):
                flash('Login successful!')
                cursor.close()
                conn.close()
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!')
        else:
            flash('Invalid username or password!')

        cursor.close()
        conn.close()

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

