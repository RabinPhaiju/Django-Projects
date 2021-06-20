1. available sub-commands
   -> django-admin

2. Create project
   ->django-admin startproject [project_name]

3. cd [project_name]

4. create new app
   -> django-admin startapp [app_name]
   -> after adding new app we have to include this in INSTALLED_APPS insilde settings.

5. run server
   -> python manage.py runserver 8000

6. before run server , we have to migrate
   -> python manage.py migrate
   -> python manage.py makemigrations

7. to login backend, we need to create a superuser
   -> python manage.py createsuperuser
