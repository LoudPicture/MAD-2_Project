The complete WebApp runs only on Linux system.
Please download the Mail Hog application (Fake SMTP server) for your system, not be linux version. 
One can run the full WebApp in WSL and run the MailHog server in Windows.


Before we could use the web app, we need to setup the environment and servers for it.
1) Setting up the Flask server :  
   - In a new Linux terminal tab, start the Flask server by typing 

             python3 main.py

2)  Setting up Redis server :     
    - In a new Linux terminal tab, start the redis server by typing 

          redis-server
    
3)  Setting up Celery Worker and Celery Beat : 
    - In a new Linux terminal tab, start the Celery Workers and Beat together by typing 
    
          celery -A tasks.celery worker -l info -B    

4) For starting MailHog - 

		~/go/bin/MailHog


The application can be tested using a test user.. Below are the credentials for the same

For admin:
username = admin'  # Case sensitive
password = '123'  .

For user:
username = 'Nikhil'  # Case sensitive
password = '234'  
