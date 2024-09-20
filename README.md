# Django

- **Create project** - (django-admin startproject [project_name])

- **Create new app** - (python manage.py startapp [app_name])
  - Django project is made up of one or more applications in folders.

- **Check code error** - (python manage.py check)

- **Run server** - (python manage.py runserver)

- **Before run server** - if you have changes in models.py
  - **makemigrations** reads all models.py -> creates/evolves the migration files -> guide by settings.py
  - **migrate** reads all migrations folders in all apps -> creates/evolves tables in db.
  - python manage.py makemigrations
  - python manage.py migrate

- **Create a superuser** - (python manage.py createsuperuser)
  
- **Model View Controller**
  - We name the three basic functions of an application as follows
  - Controller - The code that does the thinking and decision making
  - View - The HTML, CSs, etc. which makes up the look and feel of the application
  - Model - The persistent data that we keep in the data store

- **Test sql album,artist,genre,track**
  - sqlite -> sqlite3 db.sqlite
  - tables -> .tables
  - schema -> .schema [table_name]

- **Run sql command in terminal**
  - python manage.py shell
  - from Shortner.models import Artist,Genre,Album,Track;
  - Insert new Artist
    - zep = Artist(name='Rabin Phaiju')
    - zep.save()
    - zep.id
  - Look the table
    - Artist.objects.values()
  - Insert new Album
    - made = Album(title='WHo made it',artist=zep)
    - made.save()
  - Insert new Genre
    - rock = Genre(name='Metal')
    - rock.save()
  - Insert new Track
    - track_1 = Track(title='Black dog',rating=5,length = 300,count=6,album=made,genre=rock)
  - print track and foreign_key
    - first_track = Track.objects.values()
    - print(first_track)
    - print(first_track.rating)
    - print(first_track.genre)
    - print(first_track.genre.name)
    - print(first_track.album)
    - print(first_track.album.artist)
    - print(first_track.album.artist.name)
  - filter or selecting
    - track1 = Track.objects.get(pk=1)
    - track1.title | track1.rating

- **Load script**
  - python manage.py runscript [script_name] # without .py or folder_name

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
