from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from model import get_recommendations
from database import create_tables, add_user, get_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'yoursecretkey'  # Change this to a secure key

# Initialize the database
create_tables()

@app.route('/')
def landing_page():
    # Redirect to landing page if the user is not logged in
    if 'username' not in session:
        return render_template('landing_page.html')
    return redirect(url_for('recommend_page'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        favorite_genre = request.form['favorite_genre']

        # Hash the password with the updated method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        add_user(username, hashed_password, favorite_genre)

        # Automatically log in the user
        user = get_user(username)
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['favorite_genre'] = user[3]

        flash('Registration successful! Here are some movie recommendations based on your favorite genre.')

        # Redirect to the recommendations page
        return redirect(url_for('recommend_page'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['favorite_genre'] = user[3]
            flash('Login successful!')
            return redirect(url_for('recommend_page'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        favorite_genre = session.get('favorite_genre')
        return render_template('profile.html', username=session['username'], favorite_genre=favorite_genre)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('favorite_genre', None)
    flash('You have been logged out.')
    return redirect(url_for('landing_page'))

@app.route('/recommend_page')
def recommend_page():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect(url_for('landing_page'))

    genre = session.get('favorite_genre', 'all')
    recommendations = get_recommendations(genre, None)  # No minimum rating filter

    return render_template('recommend_page.html', recommendations=recommendations)

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.json.get('genre')
    rating = request.json.get('rating')

    # Use the user's favorite genre if no genre is selected
    if not genre or genre == 'all':
        genre = session.get('favorite_genre', 'all')

    recommendations = get_recommendations(genre, rating)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
