from fav_products.models import Product, Fav

from django.views import View
from django.views import generic
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from myarticles.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class ProductListView(OwnerListView):
    model = Product
    template_name = "favs/list.html"

    # overide get request defined in myarticles->ownerlistview.
    def get(self, request) :
        product_list = Product.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_products.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        ctx = {'product_list' : product_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)

class ProductDetailView(OwnerDetailView):
    model = Product
    template_name = "favs/detail.html"

class ProductCreateView(OwnerCreateView):
    model = Product
    fields = ['title', 'text']
    template_name = "favs/form.html"

class ProductUpdateView(OwnerUpdateView):
    model = Product
    fields = ['title', 'text']
    template_name = "favs/form.html"

class ProductDeleteView(OwnerDeleteView):
    model = Product
    template_name = "favs/delete.html"

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Product, id=pk)
        fav = Fav(user=request.user, product=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Product, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, product=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

