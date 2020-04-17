# First-time Setup
1. Ensure the correct version of Python is installed
	1. Run `python3 --version`
	2. This application requires Python 3.6.2 to run. If a lower version is installed, update Python; this application will not work on lower versions. If a higher version is installed, this application *may* work, but functionality is not guaranteed.
2. Install Flask and Flask-RESTful
	1. Run `python3 -m venv venv` to create a virtual environment.
	2. Run `. venv/bin/activate` to activate the virtual environment.
	3. Run `pip install Flask` to install Flask
	4. Run `pip install flask-restful` to install Flask-RESTful
3. Install coverage
	1. Run `pip install coverage` to install coverage
	2. Coverage supplements python's built-in `unittest` package. Its most important usage as far as this project is concerned is the generation of code coverage statistics. Unit test running will be discussed below.

# Unit Testing
* To run all unit tests:
	1. Run `. venv/bin/activate` to activate the virtual environment if venv has not already been activated
	2. Run `python3 -m unittest discover -v -p "*_test.py" -s src`
* To view code coverage statistics:
	1. Run `. venv/bin/activate` to activate the virtual environment if venv has not already been activated
	2. Run `coverage run -m unittest discover -p "*_test.py" -s src` to generate the statistics
	3. Run `coverage report` to view the statistics.