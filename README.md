# hungryhelpers

Software required:
- Python 3.7 or above
- Django 3.1.7
- django-localflavor (install by running 'pip install django-localflavor')
- django-environ 0.4.5 (install by running 'pip install django-environ')
- requests 2.25.1 (install by running 'pip install requests')
- django-cripsy-forms (install by running 'pip install django-crispy-forms')
- django_notifications_hq (install by running 'pip install django_notifications_hq')
- django-input_export (install by running 'pip install django-import-export')
- openpyxl (install by running 'pip install openpyxl')
- django-extensions (install by running 'pip install django-extensions')

Software execution instructions:
1. Using a command line interpreter, navigate to the root directory of the project
2. Navigate into the 'hungryhelpers' folder (hungryhelpers/hungryhelpers) and make a new file named ".env"
3. In ".env", enter "GOOGLE_MAPS_API_KEY=<b>API_KEY</b>", where <b>API_KEY</b> is the key given at the bottom of the group retrospective.
4. Return to the root directory and run the following command 'python manage.py runscript populateDB'
5. Open an internet browser and navigate to 'http://127.0.0.1:8000/'
6. Optional: Log in as an admin using 'admin' for the username and password.

Features:
- Find Location:
	- Description:
		Allows the user to pick a location to pick up their food.
	- URLs: 
		http://127.0.0.1:8000/findLocation/ 
	- Test suite execution instructions:
		1. Using a command line interpreter, navigate to the root directory of the project
		2. Run 'python manage.py test findLocation'
		3. Details about each test can be found inside the /findLocation/tests.py file.
- Account management:
	- Description: Enables users to create accounts, login, and logout. Usernames are unique to each user and passwords must be complex when creating an account (details about password requirements can be found on the signup page). Users can change password if they have an account. If users forgot their password, they will be emailed a link to be able to change their password. Users are shown a unique homepage if login is successful. Signed out users will be told that they are not logged in, and gives the user the option to log in with an existing account or create a new one. Allows users to edit personal settings such as their username, email, first name, and last name. Users may also edit their profile to add students (children) as well as update their location information. Student profile information includes name, age, school, grade, student id, and dietary/preference information. A meal plan can be created for each student to determine pickup type, day, time, and location. Meal plans can be sent and viewed by staff when the appropriate checkbox is selected.
	- URLs: 
		- http://127.0.0.1:8000/accounts/login/
		- http://127.0.0.1:8000/accounts/signup/
		- http://127.0.0.1:8000/accounts/logout/ 
		- http://127.0.0.1:8000/accounts/profile/ 
		- http://127.0.0.1:8000/accounts/edit_profile/
		- http://127.0.0.1:8000/accounts/add_student/
		- http://127.0.0.1:8000/accounts/<int:pk>/edit_student/
		- http://127.0.0.1:8000/accounts/<int:pk>/delete_student/
		- http://127.0.0.1:8000/accounts/meal_plans/
		- http://127.0.0.1:8000/accounts/<int:pk>/edit_meal_plan/
		- http://127.0.0.1:8000/accounts/settings/ 
		- http://127.0.0.1:8000/accounts/password_change/
		- http://127.0.0.1:8000/accounts/password_change/done/
		- http://127.0.0.1:8000/accounts/password_reset/
		- http://127.0.0.1:8000/accounts/password_reset/done/
		- http://127.0.0.1:8000/accounts/reset/MQ/set-password/
		- http://127.0.0.1:8000/accounts/reset/done/
	- Test suite execution instructions:
		1. Using a command line interpreter, navigate to the root directory of the project
		2. Run 'python manage.py test accounts'
		3. Details about each test can be found inside the /accounts/tests.py file.
- Parse Data:
	- Description: Created a parser for a CSV file. Parses the student information with sample student data. 
	- Testing:
		1. Using a command line interpreter, navigate to the root directory of the project and cd into the hungryhelpers directory
		2. Run 'python parseTest.py'
		3. Details about each test can be found inside the parseTest.py file
- Forgot Password:
	- Description: Allows users to change their password if they have an account. If the user forgets their password while logging on, they can click the "Forgot Password" button and an email will be sent to the user to allow them to rest their password.
	- Testing Forgot Password email verification (currently only for development):
		1. To view email, after cloning repo, navigate to the folder where the project is saved on your local machine using the file exporer (ex) /hungryhelpers/sent_emails)
		2. Open 'send_emails' folder and click on the latest log file
		3. Copy the link in that email onto the web browser
		4. Follow instructions and reset password
- Permissions
	- Description:
		Creates different permissions for users depending who they are (staff, admin, or parent)
	- Testing:
		1. Using a command line interpreter, navigate to the root directory of the project and cd into the hungryhelpers directory
		2. Run 'python manage.py test accounts.tests.PermissionsTest'
	- Creating Users:
		1. Create a user using the regular signup procedure	
		2. Log out and login as an admin and go to http://127.0.0.1:8000/admin/ 
		3. Change the permissions of the new account using the interface in the admin page
		4. Add Groups and add specific permissions (such as 'Can add google maps response')
		5. You can then add certain groups to users and once they log in, their account should adjust accordingly
- Notifications:
	- Description:
		Allows admin users to send notifcations to individual regular users
	- URLs: 
		http://127.0.0.1:8000/notifs/ 
	- Test suite execution instructions:
		1. Using a command line interpreter, navigate to the root directory of the project
		2. Run 'python manage.py test notifs'
		3. Details about each test can be found inside the /notifs/tests.py file.
	- Manual demonstration:
		1. From a browser, navigate to http://127.0.0.1:8000/ and log into the admin account (username: admin, password: admin)
		2. From a different browser, navigate to http://127.0.0.1:8000/ and create a user account
		3. From browser with the admin account logged in, navigate to http://127.0.0.1:8000/notifs/ 
		4. Enter a message to be sent to the other user and click send
		5. In the second browser, refreshing the page and clicking on the bell icon will show the notification that has been sent
		
- Meal Plans
	- Description:
	  Allows admin/staff to create new meal entries and associate them with existing pickup locations. 
	- URLs:
	  http://127.0.0.1:8000/mealPlan/
	  http://127.0.0.1:8000/mealPlan/ticket_add
	  http://127.0.0.1:8000/mealPlan/staffPage/
	  http://127.0.0.1:8000/mealPlan/send_confirm_notif/
	- Test suite execution instructions:
		1. Using a command line interpreter, navigate to the root directory of the project
		2. Run 'python manage.py test mealPlan'
		3. Details about each test can be found inside the /mealPlan/tests.py file.
	- Manual demonstration:
		1. From a browser, navigate to http://127.0.0.1:8000/ and log into the admin account
		2. Navigate to http://127.0.0.1:8000/mealPlan and fill out the provided field
		3. Entering information and clicking "Submit" will update the list of meal plans
		4. From another browser, create a regular user account, add a student, and create a meal plan for the student.
		5. From the admin browser, navigate to http://127.0.0.1:8000/mealPlan/staffPage and select "Confirm" on the new entry.
		6. From the user browser, check notifications to see the meal plan update and a link to the respective meal.
