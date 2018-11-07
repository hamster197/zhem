"""zhem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from django.conf import settings
from django.conf.urls.static import static
#handler404='zhem.views.v404_view'
#handler500='zhem.views.v404_view'
#handler404='mysite.views.my_custom_page_not_found_view'
urlpatterns = [
    #url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    #url(r'^admin', admin.site.urls),
    url(r'^$', views.login_view, name='login'),
    url(r'^accounts/login/$', views.login_view, name='login'),
    url(r'^ch_pass$', views.ch_pass_view, name='ch_login'),
    url(r'^', include('crm.urls')),
    url(r'^zvonki/', include('zvonki.urls'))

]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#if settings.DEBUG:
    #if settings.MEDIA_ROOT:
    #+ urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #+urlpatterns += staticfiles_urlpatterns(),



