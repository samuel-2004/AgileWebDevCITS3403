# NewHome
This is a web application for a "buy nothing" page. 
Users can submit items they wish to give away to others.
They can also see what items others have posted to the website and make a request for them.

# Team Members
Student Number | Student Name | GitHub Username
--- | --- | --- 
23361516 | Matthew Pfleger | MattPfleger
23366527 | Samuel Lewis  | samuel-2004
23403302 | Johnson Che | Johnny-2003
23409801 | Joel Brooker | j-brkr

# Summary
Here will be a brief summary of the architecture of the application.

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
Here will be instructions for how to run the tests for the application.

For Unit Tests:
Run: python -m unittest tests.py