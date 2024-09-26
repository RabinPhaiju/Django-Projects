from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
import datetime

# Create your views here.
@require_http_methods(['GET', 'POST'])
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def special_case_2003(request):
    return HttpResponse("special_case_2003")

def year_archive(request, year, foo):
    archive_url = reverse('year-archive', args=[2003])
    html = f'<a href="{archive_url}">2003 Archive | Special case</a>'
    return HttpResponse(f"year_archive, {year} {foo} {html}")

def month_archive(request, year, month):
    return HttpResponse(f"month_archive, {year}, {month}")

def article_detail(request, year, month, slug):
    return HttpResponse(f"article_detail, {year}, {month}, {slug}")

def page(request, num=1):
    return HttpResponse(f"page, {num}")