from flask import render_template, send_from_directory
from app import flaskApp
import sqlite3
#Since we are using os, avoid importing as much as possible
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

@flaskApp.route('/', methods=['GET'])
@flaskApp.route('/index', methods=['GET'])
@flaskApp.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')

@flaskApp.route('/advancedsearch') #, methods=('GET', 'POST') # put that after '/create' and before )
@flaskApp.route('/advancedsearch.html')
def advancedSearch():
    return render_template('advancedsearch.html')

@flaskApp.route('/search', methods=['GET'])
@flaskApp.route('/search.html', methods=['GET'])
def search():
    return render_template('search.html')

# Try the main directory if a file is not found in the root branch
@flaskApp.route('/<path:filename>')
def get_file(filename):
    # Check if the file exists in the original directory
    original_path = os_join(flaskApp.static_folder, filename)
    if os_pathexists(original_path):
        return send_from_directory(flaskApp.static_folder, filename)
    
    # If not found, try to locate the file in the directory of the Flask app
    app_directory_path = os_dirname(os_abspath(__file__))
    app_file_path = os_join(app_directory_path, filename)
    if os_pathexists(app_file_path):
        return send_from_directory(app_directory_path, filename)

    # If the file is not found in either location, return a 404 error
    return "File not found", 404

'''
con = sqlite3.connect("tutorial.db")
cur = con.cursor()
cur.execute("CREATE TABLE movie(title, year, score)")
command = ""
cur.execute(command)
#if insert:
con.commit()
con.close() #finish with this

for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
    print(row)

data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
#dont forget con.commit
'''



'''
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

    
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)    
'''