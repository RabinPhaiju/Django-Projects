1. available sub-commands
   -> django-admin

2. Create project
   ->django-admin startproject [project_name]

3. cd [project_name]

4. create new app ---> Django project is made up of one or more applications in folders.
   -> django-admin startapp [app_name]
   -> OR -> python manage.py startapp [app_name]
   -> after adding new app we have to include this in INSTALLED_APPS insilde settings.

5. check error your code
   -> python manage.py check

6. run server
   -> python manage.py runserver 8000

7. before run server | Model to Database
   -> # Makemigrations reads all models.py -> creates/evolves the migration files -> guide by settings.py
   -> # Migrate reads all migartions folders in all apps -> creates/evolves tables in db.
   -> python manage.py makemigrations
   -> python manage.py migrate

8. to login backend, we need to create a superuser
   -> python manage.py createsuperuser

9. Model View Controller

   - We name the three basic functions of an application as follows
   - Controller - The code that does the thinking and decision making
   - View - The HTML, CSs, etc. which makes up the look and feel of the application
   - Model - The persistent data that we keep in the data store

10. Test sql album,artist,genre,track

    - sqlite -> sqlite3 db.sqlite
    - tables -> .tables
    - schema -> .schema [table_name]

11. Run sql command in terminal

    - python manage.py shell
    - from Shortner.models import Artist,Genre,Album,Track;
    - Insert new Artist
      - zep = Artist(name='Rabin Phaiju')
      - zep.save()
      - zep.id
    - Look the talbe
      - Artist.objects.values()
    - Insert new Album
      - made = Album(title='WHo made it',artist=zep)
      - made.save()
    - Insert new Genre
      - rock = Genre(name='Metal')
      - rock.save()
    - Insert new Track
      - track_1 = Track(title='Black dog',rating=5,length = 300,count=6,album=made,genre=rock)
    - print track and foreignkey
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

12. Load script
    - python manage.py runscript [script_name]
