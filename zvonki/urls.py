from django.conf.urls import url

from . import views

app_name = 'zvn'

urlpatterns = [
    url(r'^index/', views.zv_index_view,  name='index'),
    #url(r'^edit/(?P<idd>[0-9]+)/$', views.edit_zvn_view, name='edit'),
    url(r'^perez/(?P<idd>[0-9]+)/$', views.pr_status_zvn_view, name='perez'),
    url(r'^nd/(?P<idd>[0-9]+)/$', views.nd_status_zvn_view, name='nd'),
    url(r'^work/(?P<idd>[0-9]+)/$', views.work_status_zvn_view, name='work'),
    url(r'^arh/(?P<idd>[0-9]+)/$', views.arh_status_zvn_view, name='arh'),
    url(r'^all/(?P<idd>[0-9]+)/$', views.for_all_status_zvn_view, name='all'),
    #url(r'^new/$', views.new_tel_save_view, name='new')
    ]