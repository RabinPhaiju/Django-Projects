from myarticles.models import Article
from myarticles.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView


class ArticleListView(OwnerListView):
    model = Article
    # By convention:
    # template_name = "myarticles/article_list.html"


class ArticleDetailView(OwnerDetailView):
    model = Article


class ArticleCreateView(OwnerCreateView):
    model = Article
    fields = ['title', 'text']


class ArticleUpdateView(OwnerUpdateView):
    model = Article
    fields = ['title', 'text']


class ArticleDeleteView(OwnerDeleteView):
    model = Article
