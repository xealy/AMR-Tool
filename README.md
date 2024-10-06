# EGH400-AMR-Project
Repository for EGH455 AMR Project

## Dashboard web app
To run the web app, I suggest you use a virtual environment to keep package installations confined to an environment. For this, first install Anaconda and follow the next steps.

### To set up conda environment:
* conda create --name egh400-env python=3.11
* conda activate egh400-env
* pip install -r requirements.txt

### To run flask app:
* first navigate to the directory that contains 'main.py'
* export FLASK_APP=main.py (if you use Mac)
* set FLASK_APP=main.py (if you use Windows -> you may also need to run $env:FLASK_APP="main.py")
* flask run
