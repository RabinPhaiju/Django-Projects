# Django App

- ## Adding new app

  - python3 manage.py startapp [app_name]
  - after adding new app we have to include this in INSTALLED_APPS inside settings.
  - App can be added in two ways:
    - **Using the app's name**: Simply add the app's name as a string.
    - **Using the app's configuration class**: You can add the app using the full path to its configuration class. This approach gives you more flexibility if your app has a custom configuration

- ## Make migrations - (python3 manage.py makemigrations [app_name])

  - By running makemigrations, you’re telling Django that you’ve made some changes to your models.
  - The makemigrations command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py.

- ## Check migration - (python3 manage.py check)

  - Check for any model changes that need to be made.

- ## Migrate - (python3 manage.py migrate)

  - apply all migrations
  - run the migrations for you and manage your database schema automatically.
  - The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your mysite/settings.py.
  - Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data.

- ## Add app to admin Dashboard

  - Tell the admin that new app having model have an admin interface.
  - open the app/admin.py
    - admin.site.register([app_model_name])

