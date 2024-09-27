from django.urls import path
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required, permission_required
=======

>>>>>>> c296fdb (added django5.1 tutorial)
from . import views

app_name = "polls" 
# if app_name is specified. {% url path_name %} will not work. change it to {% url app_name:path_name %}
<<<<<<< HEAD
# urlpatterns = [
#     # ex: /polls/
#     path("", views.index, name="index"),
    
#     # ex: /polls/5/
#     path("<int:question_id>/", views.detail, name="detail"),
#     # the name "detail" is used in the {% url %} template tag in views.py
#     # To change the path name, change the "/custom/<int:question_id>/"

#     # ex: /polls/5/results/
#     path("<int:question_id>/results/", views.results, name="results"),
    
#     # ex: /polls/5/vote/
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]

### Using generic views
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

    # File upload
    path("upload/", views.upload_file, name="upload_file"),
<<<<<<< HEAD

    # Image upload
    path("upload_image/", views.upload_image, name="upload_image"),

    # path("contact/",views.contactForm,name="contact"),
    # path("contact/",views.contactFormset,name="contact"),
    path('contact/',views.ContactFormView.as_view(),name="contact"),

    path("my_view",login_required(views.MyView.as_view()),name="my_view"),
    path("my_async",views.AsyncView.as_view(),name="my_async"),
=======
>>>>>>> 202b9c5 (added file upload)
]
# Note that the name of the matched pattern in the path strings of the second and third patterns has changed from <question_id> to <pk>. This is necessary because we’ll use the DetailView generic view to replace our detail() and results() views, and it expects the primary key value captured from the URL to be called "pk".
=======
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # the name "detail" is used in the {% url %} template tag in views.py
    # To change the path name, change the "/custom/<int:question_id>/"

    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
>>>>>>> c296fdb (added django5.1 tutorial)
