from django.urls import path, reverse_lazy
from . import views

# In urls.py reverse_lazy('fav_products:all')
# In views.py class initialization reverse_lazy('fav_products:all')
# In views.py methods reverse('fav_products:all')
# In templates {% url 'fav_products:product_update' product.id %}

app_name='fav_products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='all'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create', 
        views.ProductCreateView.as_view(success_url=reverse_lazy('fav_products:all')), name='product_create'),
    path('product/<int:pk>/update', 
        views.ProductUpdateView.as_view(success_url=reverse_lazy('fav_products:all')), name='product_update'),
    path('product/<int:pk>/delete', 
        views.ProductDeleteView.as_view(success_url=reverse_lazy('fav_products:all')), name='product_delete'),
    path('product/<int:pk>/favorite', 
        views.AddFavoriteView.as_view(), name='product_favorite'),
    path('product/<int:pk>/unfavorite', 
        views.DeleteFavoriteView.as_view(), name='product_unfavorite'),
]

