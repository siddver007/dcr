# django-celery-redis-async-server-alpha
django-celery-redis-async-server  This is a django project with a django app to give you the idea how celery can be used with django to create an API server to handle async requests. This Django-server let's you create requests running for a specified time, get running requests, kill a specific request, and get time remaining for the active requests. This is a fairly basic example with the motive of only showing how celery can be used with Django to create a Top-Notch RESTful server.


-----------------------------------------------------HOW TO RUN--------------------------------------------------------------

NOTE: For Linux(ubuntu distros only)-- Tested on ElementaryOS

1. Download the zip & extract OR clone the repository.

2. Install Python version 2.7.x where 0 <= x <= 11.

3. Install pip.

4. Install Virtual Environment( For your own benefit of not installing packages globally )
		$ pip install virtualenv

5. Create a virtual environment( Make it somewhere near the downloaded folder for your own benefit)
		$ virtualenv myvenv

		--The above Terminal initializes a virtual environment( Folder ) with name 'myvenv'
		--You can give any name

6. Install Redis Server( This is the broker which helps in message passing. It also helps in storing Celery tasks)
		$ sudo apt-get install redis-server

		--In order to execute the above command you might need to repository listing.
		--You can also install redis server by downloading the files from their website.

7. Check whether Redis Server is running or not
		$ redis-cli ping

		--If Redis Server is running then it would respond you with "PONG"

8. Enter virtual environment
		$ source PATH-TO-VIRTUAL-ENVIRONMENT/myvenv/bin/activate

		--Now the command shell would look like
			(myvenv) $

9. Install all the Project Dependencies inside virtual environment
		(myvenv) $ pip install -r requirements.txt

		--This file is inside the downloaded Project folder so either get inside the Downloaded project folder or
		  use "pip install -r PATH-TO-requirements.txt-Folder/requirements.txt"

10. Get inside the Extracted Folder(Where "manage.py" is located)

11. Start Celery workers
		(myvenv) $ ./manage.py celery worker --loglevel=info

12. Start Django project by firing up Django Server
		(myvenv) $ ./manage.py runserver 0.0.0.0:8000

		--Now Django app is running on http://localhost:8000
		--You can also access this server from any other system on the same Network


---------------------------------------------------HOW TO USE--------------------------------------------------------------

1. Creating a request
		GO TO URL -- "http://localhost:8000/api/request?connId=YOUR_WISH&timeOut=YOUR_WISH"

		--timeOut is in seconds.
		--The request is running in the background. You can see it executing in the Celery Terminal
		--The request here is doing very basic job. It is only to show that it is working. You can create any desired			   task by changing the task in "tasks.py" file.
		--You can see all the active/running requests by follwing the next step.

2. Getting and checking all running requests
		GO TO URL -- "http://localhost:8000/api/active"

3. To see the Server Status
		GO TO URL -- "http://localhost:8000/api/serverStatus"

4. To kill a request
		GO TO URL -- "http://localhost:8000/api/kill/"
		
		and execute a PUT request on it with a payload/data {"connId" : "YOUR_WISH"}


		--for your own convenience I have given a second option to kill the request
		--You can also simply kill a request by running a GET call on -- http://localhost:8000/api/kill?connId=YOUR_WISH
		so that don't have to use any Third party Software/Plugin/Extension to kill a task. 
