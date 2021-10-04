from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'gview'

# Note use of plural for list view and singular for detail view.
urlpatterns = [
    path('gview/',TemplateView.as_view(template_name='gview/base.html')),
    
    path('cats',views.CatListView.as_view(),name='cats'),
    path('cat/<int:pk>',views.CatDetailView.as_view(),name='cat'),

    path('dogs',views.DogListView.as_view(),name='dogs'),
    path('dog/<int:pk>',views.DogDetailView.as_view(),name='dog'),

    path('horses',views.HorseListView.as_view(),name='horses'),
    path('horse/<int:pk>',views.HorseDetailView.as_view(),name='horse'),

    path('cars',views.CarListView.as_view(),name='cars'),
    path('car/<int:pk>',views.CarDetailView.as_view(),name='car'),
]
