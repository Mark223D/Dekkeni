from django.conf.urls import url

from products.views import (
    ProductListView,
    CategorytListView,
    ProductDetailSlugView,)


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', CategorytListView.as_view(), name='categories'),
    url(r'^(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', CategorytListView.as_view(), name='subcategories'),
    url(r'^(?P<category>[\w-]+)/(?P<subcategory>[\w-]+)/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail-no-subsub'),
    url(r'^(?P<category>[\w-]+)/(?P<subcategory>[\w-]+)/(?P<slug>[\w-]+)/$', CategorytListView.as_view(), name='subsubcategories'),
    url(r'^(?P<category>[\w-]+)/(?P<subcategory>[\w-]+)/(?P<subsubcategory>[\w-]+)/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),

]
