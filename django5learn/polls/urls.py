from django.urls import path

from . import views

app_name = "polls" 
# if app_name is specified. {% url path_name %} will not work. change it to {% url app_name:path_name %}
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
    path("contact/",views.contactForm,name="contact"),
]
# Note that the name of the matched pattern in the path strings of the second and third patterns has changed from <question_id> to <pk>. This is necessary because we’ll use the DetailView generic view to replace our detail() and results() views, and it expects the primary key value captured from the URL to be called "pk".