# First-time Setup
1. Ensure the correct version of Python is installed
	a. Run `python3 --version`
	b. This application requires Python 3.6.2 to run. If a lower version is installed, update Python; this application will not work on lower versions. If a higher version is installed, this application *may* work, but functionality is not guaranteed.
2. Install Flask and Flask-RESTful
	a. Run `python3 -m venv venv` to create a virtual environment.
	b. Run `. venv/bin/activate` to activate the virtual environment.
	c. Run `pip install Flask` to install Flask
	d. Run `pip install flask-restful` to install Flask-RESTful