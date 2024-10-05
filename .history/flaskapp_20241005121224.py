from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a more secure key in production

def get_db_connection():
    conn = sqlite3.connect('/home/ubuntu/flaskapp/mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    conn = get_db_connection()
    # Check if the username already exists
    existing_user = conn.execute("SELECT * FROM user_profiles WHERE username = ?", (username,)).fetchone()
    
    if existing_user:
        flash('Username already exists. Want to log in instead?', 'error')
        return render_template('user_exists.html', username=username)

    try:
        conn.execute("INSERT INTO user_profiles (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                     (username, password, firstname, lastname, email))
        conn.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        flash('Error during registration. Please try again.', 'error')
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM user_profiles WHERE username = ? AND password = ?", (username, password)).fetchone()
    if user:
        all_users = conn.execute("SELECT * FROM user_profiles").fetchall()  # Fetch all users
        conn.close()  # Close connection
        return render_template('profile.html', user=user, users=all_users)  # Pass all users to the template
    else:
        flash('Invalid username or password. Please try again.', 'error')
        conn.close()  # Make sure to close connection
        return redirect(url_for('login'))



@app.route('/users')
def users():
    conn = get_db_connection()
    all_users = conn.execute("SELECT * FROM user_profiles").fetchall()
    conn.close()
    return render_template('users.html', users=all_users)

if __name__ == '__main__':
    app.run(debug=True)