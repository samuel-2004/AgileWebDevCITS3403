# NewHome
- This is a web application for a "buy nothing" page. 
- Users can sign-up and login securely, view their profile page and logout.
- Users can submit items they wish to give away to others, or request items that they would like.
- Authors can then delete their own posts
- They can also see what items others have posted to the website and reply to them.
- Posts can be searched for by content, recency and distance

# Team Members
Student Number | Student Name | GitHub Username
--- | --- | --- 
23361516 | Matthew Pfleger | MattPfleger
23366527 | Samuel Lewis  | samuel-2004
23403302 | Johnson Che | Johnny-2003
23409801 | Joel Brooker | j-brkr

# Dependencies
- Python and pip are required to install and run the server
- Running selenium tests requires that Chrome is installed, and it is run in WSL

# How to launch
To launch the application, perform the following steps:
1. Download the application `https://github.com/samuel-2004/AgileWebDevCITS3403/archive/refs/heads/main.zip`
2. Unzip the application
3. Install the required packages into a virtual environment using `pip install -r requirements.txt`
4. Run `export FLASK_APP="newhome.py"`
5. Create the database using `flask db upgrade`
6. Set the secret key with `export SECRET_KEY='<secret key>'`
7. Run the following command `flask run`

# Testing Instructions

For Unit Tests:
Run: `python -m unittest tests/unit.py`

For Selenium Tests:
Run: `python -m unittest tests/selenium.py`