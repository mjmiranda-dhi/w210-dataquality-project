from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dq/$', views.dq, name='dq'),   #home
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^dq/results$', views.results, name='results'),
    url(r'^progressbarupload/', include('progressbarupload.urls')),
    url(r'^ajax/preprocess_data/$', views.preprocess_data, name='preprocess_data')
]
