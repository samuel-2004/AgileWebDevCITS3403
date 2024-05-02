from flask import render_template, send_from_directory
from json import loads
import buynothing
from app import flaskApp
#Since we are using os, avoid importing as much as possible
from os.path import join as os_join, dirname as os_dirname, exists as os_pathexists, abspath as os_abspath

@flaskApp.route('/', methods=['GET'])
def index():
    items = loads('[{"nID":87241,"name":"Rice Cooker","who":"John Smith","suburb":"Downtown","imageref":"","timestamp":1679776345},{"nID":52379,"name":"Smartphone","who":"Emily Johnson","suburb":"Midtown","imageref":"","timestamp":1679818345},{"nID":10294,"name":"Laptop","who":"Michael Brown","suburb":"Uptown","imageref":"","timestamp":1679762345},{"nID":40957,"name":"Bicycle","who":"Sarah Davis","suburb":"Eastside","imageref":"","timestamp":1679790345},{"nID":78526,"name":"Television","who":"DavnID Wilson","suburb":"Westside","imageref":"","timestamp":1679720345},{"nID":63081,"name":"Coffee Maker","who":"Jessica Martinez","suburb":"Downtown","imageref":"","timestamp":1679804345},{"nID":21789,"name":"Headphones","who":"Christopher Lee","suburb":"Midtown","imageref":"","timestamp":1679748345},{"nID":95873,"name":"Backpack","who":"Jennifer Thompson","suburb":"Uptown","imageref":"","timestamp":1679734345},{"nID":37402,"name":"Digital Camera","who":"Daniel Garcia","suburb":"Eastside","imageref":"","timestamp":1679822345},{"nID":69023,"name":"Printer","who":"Olivia Hernandez","suburb":"Westside","imageref":"","timestamp":1679706345},{"nID":18396,"name":"Blender","who":"William Rodriguez","suburb":"Downtown","imageref":"","timestamp":1679692345},{"nID":54127,"name":"Smart Watch","who":"Ava Wilson","suburb":"Midtown","imageref":"","timestamp":1679678345},{"nID":76258,"name":"Gaming Console","who":"Ethan Moore","suburb":"Uptown","imageref":"","timestamp":1679664345},{"nID":89501,"name":"Tablet","who":"Sophia Anderson","suburb":"Eastside","imageref":"","timestamp":1679650345},{"nID":32095,"name":"Microwave Oven","who":"James Taylor","suburb":"Westside","imageref":"","timestamp":1679636345},{"nID":61478,"name":"Fitness Tracker","who":"Mia Thomas","suburb":"Downtown","imageref":"","timestamp":1679622345},{"nID":94602,"name":"Portable Speaker","who":"Benjamin White","suburb":"Midtown","imageref":"","timestamp":1679608345},{"nID":25814,"name":"Vacuum Cleaner","who":"Isabella Martinez","suburb":"Uptown","imageref":"","timestamp":1679594345},{"nID":70183,"name":"Kitchen Scale","who":"Alexander Johnson","suburb":"Eastside","imageref":"","timestamp":1679580345},{"nID":18347,"name":"Digital Watch","who":"Charlotte Brown","suburb":"Westside","imageref":"","timestamp":1679566345}]')
    return render_template('index.html', items=items, defaultimage='book.jpg', active_link='/')

@flaskApp.route('/advancedsearch')
def advancedSearch():
    return render_template('advancedsearch.html', active_link='/advancedsearch')

@flaskApp.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@flaskApp.route('/account')
def account():
    return render_template('account.html', username="jimmy_lee")

@flaskApp.route('/item/<int:itemID>')
def item(itemID):
    return render_template('items.html', itemID=itemID)

@flaskApp.route('/login')
def login():
    return render_template('login.html', active_link='/login')

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
