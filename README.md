# UdaciTrivia

UdaciTrivia is a trivia question database and API with a quiz game function. Trivia questions are grouped into six categories: science, art, geography, history, entertainment, and sports; and the quiz game can be played with questions from any one category or from all categories combined.

The application is locally hosted with a Python/Flask backend following PEP8 style guidelines and a Node/React frontend.

<br>

___


## Getting Started

### Dependencies and Installation

UdaciTrivia currently must be installed and run locally. Python 3.7, pip, and node should be installed for it to work.

#### **Backend**

`cd` into the backend directory and run `pip3.7 install -r requirements.txt` to install required packages. Edit variables in `models.py` to connect to a local database, then execute the following (from the backend folder) to run the application:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
python3.7 -m flask run
```
This will start the application in development mode on `http://127.0.0.1:5000/`.

#### **Frontend**

`cd` into the frontend directory and execute the following to run the frontend client:
```
npm install // only run the first time to install dependencies
npm start
```
This will start the frontend client in development mode on `http://127.0.0.1:3000/`

### Tests

To run tests, update variables in `test_flaskr.py` to connect to a local database, then `cd` to the backend folder and execute the following:
```
./testinit.sh
python3.7 test_flaskr.py
```
`testinit.sh` is a shell script that creates and preps the `bookshelf_test` database used by the test program. 

All tests are contained in the `test_flaskr.py` program, and tests should be maintained and updated there as new functionality is added to the application.

<br>

___


## API Reference

See [API Reference readme](backend/APIReference.md)

<br>

___


## Deployment

**N/A**

<br>

___


## Authors

Yours truly and the team at Udacity

<br>

___


## Acknowledgements

Thanks to everyone at Udacity, and especially to Coach Caryn for leading the API Development and Documentation course!

