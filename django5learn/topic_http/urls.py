from django.urls import include, path
from django.urls import path, re_path
from . import views

# remove redundancy
blog_patterns = [
    path("", views.page),
    path("page<int:num>/", views.page),
]

## using re to match year
# fix -> the year 10000 will no longer match since the year integers are constrained to be exactly four digits long.
urlpatterns = [
    path("", views.current_datetime, name="topic_http"),
    path("articles/2003/", views.special_case_2003),

    re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_archive,{"foo":"bar"},name='year-archive'),

    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.month_archive),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$",views.article_detail),

    # Specifying defaults for view arguments
    # path("blog/", views.page),
    # path("blog/page<int:num>/", views.page),
    ## removing the redundancy
    path("blog/", include(blog_patterns)),

]

### old way of doing it
# bugs here like 2nd line can be passed 20333 as year
# urlpatterns = [
#     path("articles/2003/", views.special_case_2003),
#     path("articles/<int:year>/", views.year_archive),
#     path("articles/<int:year>/<int:month>/", views.month_archive),
#     path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail),
# ]