# ![Http](https://docs.djangoproject.com/en/5.1/topics/http/urls/)

## Registering custom path converters

-- For more complex matching requirements, you can define your own path converters.
--Deprecated since version 5.1:
Overriding existing converters with django.urls.register_converter() is deprecated.

## Using regular expressions

If the paths and converters syntax isn’t sufficient for defining your URL patterns, you can also use regular expressions.

## Nested arguments

urlpatterns = [
    re_path(r"^blog/(page-([0-9]+)/)?$", blog_articles),  # bad
    re_path(r"^comments/(?:page-(?P<page_number>[0-9]+)/)?$", comments),  # good
]

-- Both patterns use nested arguments and will resolve: for example, blog/page-2/ will result in a match to blog_articles with two positional arguments: page-2/ and 2. The second pattern for comments will match comments/page-2/ with keyword argument page_number set to 2. The outer argument in this case is a non-capturing argument (?:...).

## Specifying defaults for view arguments

urlpatterns = [
    path("blog/", views.page),
    path("blog/page<int:num>/", views.page),
]

def page(request, num=1):
    pass

## remove redundancy

urlpatterns = [
    path("<page_slug>-<page_id>/history/", views.history),
    path("<page_slug>-<page_id>/edit/", views.edit),
    path("<page_slug>-<page_id>/discuss/", views.discuss),
    path("<page_slug>-<page_id>/permissions/", views.permissions),
]
-- to 
urlpatterns = [
    path(
        "<page_slug>-<page_id>/",
        include(
            [
                path("history/", views.history),
                path("edit/", views.edit),
                path("discuss/", views.discuss),
                path("permissions/", views.permissions),
            ]
        ),
    ),
]

## Passing extra options to view functions

urlpatterns = [
    path("blog/<int:year>/", views.year_archive, {"foo": "bar"}),
]


## Reverse resolution of URLs

urlpatterns = [
    path("articles/<int:year>/", views.year_archive, name="news-year-archive"),
]

-- html
<a href="{% url 'news-year-archive' 2012 %}">2012 Archive</a>
-- python code
def redirect_to_year(request):
    year = 2006
    return HttpResponseRedirect(reverse("news-year-archive", args=(year,)))

