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
from django.contrib.auth.decorators import login_required
from django.http import request
#from django.views.generic import DetailView,ListView

from . import views


app_name='crm'

urlpatterns = [
    #login
    url(r'^$', views.login_view,  name='login'),
    url(r'^logout/', views.logoutview, name='logout'),

    #news
    url(r'^news/$', views.zaiyavka_Index_view, name='news_index'),
    url(r'^news/(?P<idd>[0-9]+)/$',views.news_detail_view, name='news_detail'),
    url(r'^news/edit(?P<idd>[0-9]+)/$', views.news_edit_view, name='news_edit'),
    url(r'^news/newnews/$', views.news_postform, name='news_newpost'),

    #flats
    url(r'^flats/newflat/$', views.flat_postForm, name='new_flat'),
    url(r'^flats/newflat_appart/$', views.flat_apparts_postForm, name='flat_apparts_postForm'),#new flat(only for appartaments)
    url(r'^flats/myflats_pub/$', views.my_flatview_pub, name='my_flatpub'), ## All Flats
    url(r'^flats/excl_flats_pub/$', views.excl_flatview_pub, name='excl_flatpub'), ## Exclusive Flats
    url(r'^flats/allflats_pub/$', views.all_flatview_pub, name='all_flatpub'),

    url(r'^flats/vestum/pup/(?P<idd>[0-9]+)/$',views.vestum_pub_view, name='Vs_pub'),
    url(r'^flats/all_vs_pub/$', views.vestum_All_pub_view, name = 'all_vs_pub'),

    url(r'^flats/Seo_flats_pub/$', views.all_flatviewSeo_pub, name='seo_flat_pub'),
    url(r'^flats/Seo_flats_Unpub/$', views.all_flatviewSeo_unpub, name='seo_flat_unpub'),
    url(r'^flats/allflats_pub_form/(?P<idd>[0-9]+)/$', views.seo_flat_pub, name='form_flatpub'),

    url(r'^flats/myflats_unpub/$', views.my_flatview_unpub, name='my_flatunpub'),
    url(r'^flat/edit(?P<idd>[0-9]+)/$', views.my_flatview_edit, name='flat_edit'),
    url(r'^flat/(?P<idd>[0-9]+)/$', views.myflatDetail, name='flat_detail'),
    url(r'^flat/print/(?P<idd>[0-9]+)/$', views.myflatPrint, name='flat_print'),
    url(r'^newFlatGal/(?P<idd>[0-9]+)/$',views.flat_photo_new_view, name='newFlatgal'),
    url(r'^flatdel/(?P<idd>[0-9]+)/(?P<sidd>[0-9]+)/$',views.flat_del_view, name='FlatPhotodel'),
    ##feeds
    url(r'^domclick.xml$', views.YandexFeedview, name='Yandex'),#for yandex feed
    url(r'^mail.xml$', views.MailRuFeedview, name='Mail'),  # for mail.ru feed
    url(r'^grFeed.xml$', views.GRFeedview, name='Yandex'),  # for yandex feed
    url(r'^domclick1.xml$', views.domclickfeedview, name='domclick'), #for domclick
    url(r'^vestum.xml$', views.vestumfeedview, name='vestumFeed'), #for Vestum 700
    url(r'^vestum300.xml$', views.vestumfeedview300, name='vestumFeed300'),  # for Vestum 300
    url(r'^vestumHouses.xml$', views.vestumFeedViewHouses, name='vestumHouses'),  # for Vestum Houses
    url(r'^sait.xml$', views.sait_vigr_view, name='domclick'), #for sait_feed
    ##any
    url(r'^domclick_index/$', views.domclick_Index_view, name='domclick_index'),
    url(r'^kdastr/(?P<idd>[0-9]+)/$', views.kadastr_edit, name='new_kadastr'),# new_kadastr_numb

    #clients
    url(r'^clients/newclient/$', views.new_client_view, name='new_client'),
    url(r'^clients/editclient/(?P<idd>[0-9]+)/$', views.edit_client_view, name='edit_client'),
    url(r'^clients/own_clients/$', views.own_clients_view, name='own_clienws'),
    url(r'^clients/all_clients/$', views.all_clients_view, name='all_clienws'),
    url(r'^clients/otd_clients/$', views.otd_clients_view, name='otd_clienws'),
    url(r'^client/(?P<idd>[0-9]+)/$', views.cliend_detail_view, name='client_detail'),

    #doma
    url(r'^new_dom/$', views.new_dom_view, name='new_dom_post'),
    url(r'^pub_unp_dom/$', views.mu_unpob_doma_view, name='upb_dom_view'),
    url(r'^pub_pub_dom/$', views.mu_pob_doma_view, name='pub_dom_view'),
    url(r'^doms/(?P<idd>[0-9]+)/$',views.dom_detail_view,name='dom_detail'),
    url(r'^doms/edit(?P<idd>[0-9]+)/$', views.domaeditview, name='dom_edit'),
    url(r'^doms/print/(?P<idd>[0-9]+)/$',views.dom_print_view,name='dom_print'),

    #uchastki
    url(r'^new_uch/$', views.new_uc_view, name='new_uch_post'),
    url(r'^pub_uch/$',views.pup_uchastki,name='pub_uc_index'),
    url(r'^un_uch/$',views.unpup_uchastki,name='unpub_uc_index'),
    url(r'^uch/(?P<idd>[0-9]+)/$',views.uch_detail_view,name='uc_detail'),
    url(r'^uchprt/(?P<idd>[0-9]+)/$',views.uch_print_view,name='uc_print'),
    url(r'^uch/edit(?P<idd>[0-9]+)/$', views.ucheditview, name='uc_edit'),

    #otchet
    url(r'^newotchet/$',views.new_otchet_view_All, name='otch_new_all'),
    url(r'^editotchet/(?P<idd>[0-9]+)/$', views.otchet_edit_view, name='otch_edit'),
    url(r'^allochet/$',views.reeelt_otchet_all_view, name='otch_all_reelt'),
    url(r'^sdelka/(?P<idd>[0-9]+)/$', views.reelt_sdelka_otchet_detail_view, name='otch_detail'),
    url(r'^sdelka/zakrit/(?P<idd>[0-9]+)/$',views.sdelka_zakritie_view, name='sdelka_zakr'),
    url(r'^sdelka/sriv/(?P<idd>[0-9]+)/$',views.sdelka_sriv_view, name='sdelka_sriv'),
    url(r'^sdelka/rasr/(?P<idd>[0-9]+)/$',views.sdelka_rasroch_view, name='sdelka_rasr'),
    url(r'^sdelka/delete/(?P<idd>[0-9]+)/$',views.sdelka_delete_view, name='sdelka_del'),
    url(r'^totchet/$', views.tempFioView,name='1'),#all fio in sdelka edit
    url(r'^testotch/$',views.kach_otch_view,name='DmCahestvoOtch'), #temp for domck kachestvo
    url(r'^perenos_groups/$',views.temp_otch_view, name='tempGroupOtchet'), #for perenos groups

    # feeds
    url(r'^cian.xml$', views.cianfeedview, name='cian'),
    url(r'^megareal.xml$', views.MegaRealfeedview, name='mega'),
    url(r'^new/$',views.newvigrView, name='newvigr'),
    url(r'^nnew/$',views.newvigrNovostroikaView , name='newNovvigr'),
    url(r'^newviggal/(?P<idd>[0-9]+)/$',views.newVigGalView, name='newvigrgal'),
    url(r'^cianindex/$', views.cianindexview, name='cianindex'),
    url(r'^cianindexup/$', views.cianindexUPview, name='cianindexupl'),
    url(r'^cianedit/(?P<idd>[0-9]+)/$',views.cianedit, name='cianedit'),
    url(r'^ciandels/(?P<idd>[0-9]+)/$',views.cianDelviewSubjct, name='ciandelsubj'),
    url(r'^ciandel/(?P<idd>[0-9]+)/(?P<sidd>[0-9]+)/$',views.ciandelview, name='ciandel'),

    #Zayavki
    url(r'^zayavka/new/$',views.New_Zayavka_View, name='NewZayav'),
    url(r'^zayavka/new_nov/$', views.New_Nov_Zayavka_View, name='NewZayavNov'),
    url(r'^zayavka/new_nov_lich/$', views.lich_rielt_Zayavka_View, name='NewZayavLich'),
    url(r'^index/$',views.zaiyavka_Index_view, name='indexZayavka'),
    url(r'^zayavka/vzyat/(?P<idd>[0-9]+)/$', views.zayavka_vzyata_view, name='VzyatZayav'),
    url(r'^zayavka/sdelka/(?P<idd>[0-9]+)/$', views.zayavka_sdelka_view, name='SdelkaZayav'),
    url(r'^zayavka/sriv/(?P<idd>[0-9]+)/$', views.zayavka_sriv_view, name='SdelkaSriv'),

    #statistika
    url(r'^stat_obj/$', views.stat_count_crm_obj, name='crm_obj_index'),
    url(r'^stat_obj_past/$', views.stat_count_crm_obj_past, name='crm_obj_past_index'),
    url(r'^sdelkaReit/$', views.reyting_po_sdelkam_view, name = 'sdelka_reit'),
    url(r'^sdelkarieltMonthSearch/$', views.reyting_po_sdelkam_mSearch_view, name='sdelkarieltMonthSearch'),
    url(r'^sdelkarieltKvSearch/$', views.reyting_po_sdelkam_mSearch_view, name='sdelkarieltKvSearch'),
    url(r'^sdelkarielt2KvSearch/$', views.reyting_po_sdelkam_2Kvartal_view, name='sdelkarielt2KvSearch'),
    url(r'^sdelkarielt3KvSearch/$', views.reyting_po_sdelkam_3Kvartal_view, name='sdelkarielt3KvSearch'),
    url(r'^sdelkarielt4KvSearch/$', views.reyting_po_sdelkam_4Kvartal_view, name='sdelkarielt4KvSearch'),
    url(r'^sdelkarieltGodSearch/$', views.reyting_po_sdelkam_tek_god, name='sdelkarieltGodSearch'),

    #for homka admin
    url(r'^myadm/$', views.my_admi_view, name = 'myadm'),

    # for Dashboard
    url(r'^dashboard/$', views.DashBoardView, name='DashBoard'),

    #Domcklic texts
    url(r'^dm/index/$', views.dmIndexView, name='dm_index'),
    url(r'^dm/edit/(?P<idd>[0-9]+)/$', views.EditDMtextView, name='dm_edit'),
    url(r'^dm/new/$', views.newDMtextView, name='dm_new'),

    ]
