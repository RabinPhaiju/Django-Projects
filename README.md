1. available sub-commands
   -> django-admin

2. Create project
   ->django-admin startproject [project_name]

3. cd [project_name]

4. create new app
   -> django-admin startapp [app_name]
   -> OR -> python manage.py startapp [app_name]
   -> after adding new app we have to include this in INSTALLED_APPS insilde settings.

5. check error your code
   -> python manage.py check

6. run server
   -> python manage.py runserver 8000

7. before run server , model to database
   -> migrate takes care about which database to create specified in setting.py
   -> python manage.py migrate
   -> python manage.py makemigrations

8. to login backend, we need to create a superuser
   -> python manage.py createsuperuser
