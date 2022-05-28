from django.conf.urls import include
from django.urls.conf import re_path
from rest_framework import routers

from .views import ProductViewSet, ProductsListView, ProductsUpdateView, ProductCreateView, product_import, store_create, category_create, ProductView, ProductsBuyView

app_name = 'commercial'

router = routers.DefaultRouter()
router.register(r'product_list', ProductViewSet)

urlpatterns = [
    re_path('^api/', include(router.urls)),
    re_path('^ajax/post/product/(?P<pk>\d+)/$', ProductsUpdateView.as_view(), name="ajax-product-post"),
    re_path('^product/create/$', ProductCreateView.as_view(), name="product-create"),
    re_path('^product/import/$', product_import, name="product-import"),
    re_path('^store/create/$', store_create, name="store-create"),
    re_path('^category/create/$', category_create, name="category-create"),
    re_path('^products/$', ProductView.as_view(), name="products"),
    re_path('^product/buy/(?P<pk>\d+)/$', ProductsBuyView.as_view(), name="products-buy"),
    re_path('', ProductsListView.as_view(), name="home"),
]