"""erratum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views as erratum_views
from uploads import views as uploads_views


urlpatterns = [
	url(r'^$', erratum_views.index_new, name='index_new'),
	url(r'^home.html$', erratum_views.index_new, name='index_new'),
	url(r'^admin/', admin.site.urls),
	url(r'^about.html$', erratum_views.about_new, name='about_new'),
	url(r'^hierarchical.html$', erratum_views.hierarchical_new, name='hierarchical_new'),
	url(r'^signUp.html$', erratum_views.signUp_new, name='signUp_new'),

	# Placeholder until upload functionality is tied to demo.html
	url(r'^demo.html', erratum_views.demo_new, name='demo_new'),

	url(r'^uploads/', include('uploads.urls', namespace='uploads', app_name='uploads')),

    # Added for django-registration-redux (v1.5)
    url(r'^accounts/profile', erratum_views.index_new, name='index_new'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^uploads/$', uploads_views.index, name='index'),
    url(r'^uploads/dq/$', uploads_views.dq, name='dq'),   #home
    url(r'^uploads/about$', uploads_views.about, name='about'),
    url(r'^uploads/contact$', uploads_views.contact, name='contact'),
    url(r'^uploads/dq/results$', uploads_views.results, name='results'),
    url(r'^uploads/progressbarupload/', include('progressbarupload.urls')),
    url(r'^uploads/svcs/$', uploads_views.backend_details),
    url(r'^uploads/static/(?P<path>.*)$', uploads_views.send_file, name='send_file'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'ERRATUM.IO Administration'