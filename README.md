# hungryhelpers

Software required:
- Python 3.7 or above
- Django 3.1.7

Software execution instructions:
1. Using a command line interpreter, navigate to the root directory of the project
2. Run the command 'python manage.py runserver'
3. Open an internet browser and navigate to 'http://127.0.0.1:8000/'

Features:
   - Account management: 
        - Description:
			Enables users to create accounts, login, and logout. Usernames are unique to each user and passwords must be complex when creating an account (details about password requirements can be found on the signup page). Users are shown a unique homepage if login is successful. Signed out users will be told that they are not logged in, and gives the user the option to log in with an existing account or create a new one.
		- URLs: <br />
			http://127.0.0.1:8000/accounts/login/ <br />
			http://127.0.0.1:8000/accounts/signup/ <br />
			http://127.0.0.1:8000/accounts/logout/ <br />
		- Test suite execution instructions:
			1. Using a command line interpreter, navigate to the 'accounts' folder of the project
			2. python manage.py test accounts
			3. Details about each test can be found inside the /accounts/tests.py file.