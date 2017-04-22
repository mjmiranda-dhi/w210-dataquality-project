from django.conf.urls import url
from erratum import views as base_views
from . import views

urlpatterns = [
    url(r'^$', base_views.index, name='index'),
    url(r'^success/$', views.upload_list, name='upload_list'),
    url(r'^fail/$', views.fail_list, name='fail_list'),
    url(r'^(?P<userName>[-\w]+)/$', views.upload_detail_for_user, name = 'upload_detail_for_user'),
]