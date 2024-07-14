import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Alex12357'
DATABASE = 'stories.db'

# Admin credentials (you can later improve this by storing hashed passwords in a database)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_latest_stories():
    conn = get_db_connection()
    stories = conn.execute('SELECT * FROM stories ORDER BY date DESC LIMIT 4').fetchall()
    conn.close()
    return stories

@app.route('/')
def index():
    latest_stories = get_latest_stories()
    return render_template('index.html', stories=latest_stories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('upload'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        image = request.files['image']
        content = request.form['content']

        if not category or not title or not content:
            flash('All fields are required')
            return redirect(url_for('upload'))

        filename = f"{title.replace(' ', '_')}.txt"
        image_path = None
        if image:
            image_path = f"static/images/{image.filename}"
            image.save(image_path)

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO stories (title, category, image, content, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, image_path, content, datetime.now().strftime('%B %d, %Y')))
        conn.commit()
        conn.close()

        flash('Story uploaded successfully')
        return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/category')
def category():
    return render_template('category.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
