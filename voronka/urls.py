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
from django.conf.urls import url
from . import views


app_name='voronka_ap'
urlpatterns = [
    url(r'^voronka/new_new_vh$', views.NewZayavVhView, name='voronka_new_vh_zayav'),
    url(r'^voronka/new_new_work$', views.NewZayavWorkView, name='voronka_new_work_zayav'),
    url(r'^voronka/vhedit/(?P<idd>[0-9]+)/$', views.EditZayavVhView, name='voronka_vh_edit'),
    url(r'^voronka/vhvzyat/(?P<idd>[0-9]+)/$', views.VzZayvSaitView, name='voronka_vh_vzyat_zayav'),
    url(r'^voronka/nedozvon/(?P<idd>[0-9]+)/$', views.NedozvZayvSaitView, name='voronka_nedozvon_zayav'),
    url(r'^voronka/index$', views.VoronkaIndexView, name='voronka_index'),
    url(r'^voronka/detail/(?P<idd>[0-9]+)/$', views.VoronkaDetailView, name='voronka_detail'),

    url(r'^voronka/amain$', views.MainAdmVoronkaView, name='voronka_main_adm'),
    #url(r'^voronka/changestauszayav/(?P<idd>[0-9]+)/(?P<st_id>[0-9]+)/$',
    #    views.VoronkaChangeView, name='voronka_ChangeStatus'),
    #url(r'^avito/new$', views.newAvitoSub, name='Avito_new'),
    #url(r'^avito/edit/(?P<idd>[0-9]+)/$', views.AvitoEditSubjView, name='Avito_Edit_Subj'),
    #url(r'^avito/edit/obichn/(?P<idd>[0-9]+)/$', views.AvitoBZPubView, name='Avito_Post_Obicn'),
    #url(r'^avito/edit/premium/(?P<idd>[0-9]+)/$', views.AvitoPremiumPubView, name='Avito_Post_premium'),
    #url(r'^avito/edit/VIP/(?P<idd>[0-9]+)/$', views.AvitoVIPPubView, name='Avito_Post_VIP'),
    #url(r'^avito/edit/Podn/(?P<idd>[0-9]+)/$', views.AvitoPodnPubView, name='Avito_Post_Podn'),
    #url(r'^avito/edit/Vid/(?P<idd>[0-9]+)/$', views.AvitoVidPubView, name='Avito_Post_Vid'),
    #url(r'^avito/edit/Turbo/(?P<idd>[0-9]+)/$', views.AvitoTurboPubView, name='Avito_Post_Turbo'),
    #url(r'^avito/edit/Quick/(?P<idd>[0-9]+)/$', views.AvitoQuickPubView, name='Avito_Post_Quick'),
    #url(r'^avito/Gal/(?P<idd>[0-9]+)/$', views.AvitoGalView, name='Avito_new_galery'),
    #url(r'^avito/del/(?P<idd>[0-9]+)/$', views.AvitoDellView, name='Avito_Del_Subj'),
    #url(r'^avito/Gal/del/(?P<idd>[0-9]+)/(?P<sidd>[0-9]+)/$', views.AvitiGalView, name='Avito_del_galery'),
    #url(r'^avito/avito.xml$', views.avitoFeedView, name='Avito_feed'),
]
