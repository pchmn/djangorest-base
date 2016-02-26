from django.conf.urls import url

from products import views

urlpatterns = [
    url(r'^$', views.CategoryList.as_view(), name="category_list"),
    url(r'^category/(?P<pk>[0-9]+)/$', views.ProductList.as_view(), name="product_list"),
    url(r'^(?P<pk>[0-9]+)/$', views.ProductDetails.as_view(), name="product_details"),
]
