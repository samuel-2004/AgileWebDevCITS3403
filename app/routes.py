from flask import render_template, send_from_directory
import buynothing
from app import flaskApp
#Since we are using os, avoid importing as much as possible
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

@flaskApp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@flaskApp.route('/advancedsearch') #, methods=('GET', 'POST') # put that after '/create' and before )
def advancedSearch():
    return render_template('advancedsearch.html')

@flaskApp.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@flaskApp.route('/account')
def account():
    return render_template('account.html')

@flaskApp.route('/item?<int:itemID>')
def item(itemID):
    return render_template('items.html?' + itemID)

@flaskApp.route('/login')
def login():
    return render_template('login.html')

@flaskApp.route('/upload')
def upload():
    return render_template('upload.html')

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
