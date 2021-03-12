# hungryhelpers

Software required:
- Python 3.7 or above
- Django 3.1.7

Software execution instructions:
1. Using a command line interpreter, navigate to the root directory of the project
2. Run the command 'python manage.py runserver'
3. Open an internet browser and navigate to 'http://127.0.0.1:8000/'

Features:
- Find Location:
	- Description:
		Allows the user to pick a location to pick up their food
	- URLs: 
		http://127.0.0.1:8000/findLocation/ 
	- Test suite execution instructions:
		1. Using a command line interpreter, navigate to the root directory of the project
		2. Run 'python manage.py test findLocation'
		3. Details about each test can be found inside the /findLocation/tests.py file.
- Account management:
	- Description:
		Enables users to create accounts, login, and logout. Usernames are unique to each user and passwords must be complex when creating an account (details about password requirements can be found on the signup page). Users are shown a unique homepage if login is successful. Signed out users will be told that they are not logged in, and gives the user the option to log in with an existing account or create a new one.
	- URLs: 
		- http://127.0.0.1:8000/accounts/login/
		- http://127.0.0.1:8000/accounts/signup/ 
		- http://127.0.0.1:8000/accounts/logout/ 
	- Test suite execution instructions:
		1. Using a command line interpreter, navigate to the root directory of the project
		2. Run 'python manage.py test accounts'
		3. Details about each test can be found inside the /accounts/tests.py file.
- Dashboard
	- Description:
		The dashboard allows for convenient navigation between pages and presents the user the most important information from the notifications, map/scheduler pages, and ticket submission pages
	- Testing:
		1. To view dashboard, after cloning repo, navigate to the folder the project is saved in on your local machine using the file explorer
		2. Open index.html in your browser of choice
		3. Navigation will be possible to other pages by clicking on them, pages currently contain placeholder content
- Parse Data:
	- Description: Created a parser for a CSV file. Parses the student information with sample student data. 
	- Testing:
		1. Using a command line interpreter, navigate to the root directory of the project and cd into the hungryhelpers directory
		2. Run 'python parseTest.py'
		3. Details about each test can be found inside the parseTest.py file
