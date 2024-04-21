from flask import render_template, send_from_directory
from app import flaskApp
import sqlite3
#Since we are using os, avoid importing as much as possible
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

navbar = """
    <div class="topnav" id="topnav">
      <img src="logodefault.jpg" style="width:400px;height:100px;" alt>
      <a class="active" href="/">Home</a>
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
      <a href="login">Login</a>
      <a href="advancedsearch">Search</a>
      <div class="search-container">
        <form action="search" accept-charset="UTF-8" method="get">
          <input type="text" placeholder="Search.." name="q" maxlength="1024" >
          <button type="submit"><i class="bi bi-search"></i></button>
        </form>
      </div>
    </div>
    """

#<!-- The following was derived from https://getbootstrap.com/docs/5.2/examples/footers/ -->
footer = """
<div class="container">
      <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
        <p class="col-md-4 mb-0 text-muted">&copy; 2024 Company, Inc</p>

        <a class="col-md-4 d-flex align-items-center justify-content-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
          <svg class="bi me-2" width="40" height="32"><use xlink:href="#bootstrap"/></svg>
        </a>

        <ul class="nav col-md-4 justify-content-end">
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Home</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Features</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">Pricing</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">FAQs</a></li>
          <li class="nav-item"><a href="#" class="nav-link px-2 text-muted">About</a></li>
        </ul>
      </footer>
    </div>
"""

pageElements = {"navbar": navbar, "footer": footer}


@flaskApp.route('/', methods=['GET'])
def index():
    return render_template('index.html', pageElements=pageElements)

@flaskApp.route('/advancedsearch') #, methods=('GET', 'POST') # put that after '/create' and before )
def advancedSearch():
    return render_template('advancedsearch.html', pageElements=pageElements)

@flaskApp.route('/search', methods=['GET'])
def search():
    return render_template('search.html', pageElements=pageElements)

@flaskApp.route('/account')
def account():
    return render_template('account.html', pageElements=pageElements)

@flaskApp.route('/item?<int:itemID>')
def item(itemID):
    return render_template('items.html?' + itemID, pageElements=pageElements)

@flaskApp.route('/login')
def login():
    return render_template('login.html', pageElements=pageElements)

@flaskApp.route('/upload')
def upload():
    return render_template('upload.html', pageElements=pageElements)

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