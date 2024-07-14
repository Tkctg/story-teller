import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'Alex123'
DATABASE = 'stories.db'

# Directory where the stories are stored
#STORIES_DIR = 'static/stories'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

def get_db_connection():
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  return conn

def get_latest_stories():
  stories = []
  for filename in os.listdir(STORIES_DIR):
    if filename.endswith('.txt'):  # assuming stories are stored in text files
      filepath = os.path.join(STORIES_DIR, filename)
      with open(filepath, 'r') as file:
        content = file.read()
        # Extract metadata from the file (assuming a specific format)
        title, category, excerpt, date_str = content.split('\n', 3)
        date = datetime.strptime(date_str.strip(), '%B %d, %Y')
        stories.append({
            'title': title.strip(),
            'category': category.strip(),
            'excerpt': excerpt.strip(),
            'date': date,
            'filename': filename
        })
  # Sort stories by date (latest first)
  stories.sort(key=lambda x: x['date'], reverse=True)
  return stories[:4]  # Return only the latest 4 stories


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

    # Save the story content
    filename = f"{title.replace(' ', '_')}.txt"
    with open(os.path.join(STORIES_DIR, filename), 'w',
              encoding='utf-8') as file:
      file.write(
          f"{title}\n{category}\n{content[:100]}...\n{datetime.now().strftime('%B %d, %Y')}\n{content}"
      )

    # Save the image if provided
    if image:
      image.save(os.path.join('static/images', image.filename))

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
  app.run(host='0.0.0.0', debug=True)
