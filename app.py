from flask import Flask, render_template, send_from_directory
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/advancedsearch') #, methods=('GET', 'POST') # put that after '/create' and before )
@app.route('/advancedsearch.html')
def advancedSearch():
    return render_template('advancedsearch.html')

@app.route('/search')
@app.route('/search.html')
def search():
    return render_template('search.html')

# Try the main directory that
@app.route('/<path:filename>')
def get_file(filename):
    # Check if the file exists in the original directory
    original_path = os_join(app.static_folder, filename)
    if os_pathexists(original_path):
        return send_from_directory(app.static_folder, filename)

    # If not found, try to locate the file in the directory of the Flask app
    app_directory_path = os_dirname(os_abspath(__file__))
    app_file_path = os_join(app_directory_path, filename)
    if os_pathexists(app_file_path):
        return send_from_directory(app_directory_path, filename)

    # If the file is not found in either location, return a 404 error
    return "File not found", 404
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