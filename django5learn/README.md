# Django App

- ## Adding new app

  - python3 manage.py startapp [app_name]
  - after adding new app we have to include this in INSTALLED_APPS inside settings.
  - App can be added in two ways:
    - **Using the app's name**: Simply add the app's name as a string.
    - **Using the app's configuration class**: You can add the app using the full path to its configuration class. This approach gives you more flexibility if your app has a custom configuration

- ## Make migrations 
  
  - (python3 manage.py makemigrations [app_name])
  - (python3 manage.py makemigrations --name)

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

- **Use generic views: Less code is better**
  - Generic views abstract common patterns to the point where you don’t even need to write Python code to write an app. For example, the ListView and DetailView generic views abstract the concepts of “display a list of objects” and “display a detail page for a particular type of object” respectively.

- **Automated Testing**
  - python manage.py test [app_name]
  - python manage.py test [app_name].tests.[test_name/class_name]
  - pattern file test
    - python manage.py test --pattern="test*.py"

- **Fixtures** - (python3 manage.py loaddata [path_to_fixtures ot file_name.extension])

- **Model View Controller**
  - We name the three basic functions of an application as follows
  - Controller - The code that does the thinking and decision making
  - View - The HTML, CSs, etc. which makes up the look and feel of the application
  - Model - The persistent data that we keep in the data store

- **When to use APIViews**
  - Need full control over the logic
  - Processing files and rendering a synchronous response
  - You are calling other APIs/services
  - Accessing local files or data

- **When to use ViewSets**
  - A simple CRUD interface to your database
  - A quick and simple API
  - Little to no customization on the logic
  - Working with standard data structures

- **APIViews vs GenericAPIView**
  - GenericAPIView is a class-based view
  - APIView is a function-based view
