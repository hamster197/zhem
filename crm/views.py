
import requests
import json
import calendar
import pytils
from datetime import timezone, datetime, timedelta
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import loginform, newsform, flatform, flat_search_form, newclientform, client_edit_form, doma_new_post, \
    uc_new_post, flateditform, doma_edit_form, uc_edit_form, otchet_all_form, \
    vigruzkaForm, vigruzkaGaleryForm, vigGalForm, flat_pict_form, vigruzkaNovostroikaForm, yandex_flatform, \
    yandex_flateditform, all_otchet_filtr_form, otchet_all_form1, Urist_new_zayavka_Form, sriv_zayavka_form, \
    nov_new_zayv_form, all_zayav_form, reelt_lich_new_zayv_form, search_by_moth_form, seo_pub_form, kadastr_form, \
    adm_form, DmTextForm, vestum_count_form, vestum_poryadok_form, vestum_pub_form, resep_flatform, flatform_appart
from .models import news, flat_obj, flat_obj_gal, clients, uchastok, otchet_nov, feed, feed_gallery, zayavka, \
    stat_obj_crm, reyting_po_sdelkam, reyt_sdelka_otd, cachestvoDomCl, UserProfile1, domclickText, TmpCianCount, \
    vestum_poryadok_feed


def login_view(request):
    if request.POST:
        form=loginform(request.POST)
        if form.is_valid():
            u=form.cleaned_data['username']
            p=form.cleaned_data['passw']
            user=authenticate(username = u , password = p)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('crm:news_index')


    else:
        form=loginform()
    return render(request,'crm/login.html',{'tpform':form})

#def logoutview(request):
    #logout(request)
    #return redirect('crm:login')
def logoutview(request):
    date_end = timezone.datetime.now()
    date_start = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day-1)
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name=='Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name =user.last_name + ' '+user.first_name
#################################################
##### Kol Sdelok                            ###
#################################################
                        sdelki_count = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Да',
                                                                 date_zakr__lte=date_end, date_zakr__gte=date_start).count()
#################################################
##### Kol _subj_Cian                            ###
#################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                         date_sozd__lte=date_end, date_sozd__gte=date_start).count()
#################################################
##### Kol Subj CRM                            ###
#################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                                 #date_sozd__lte=date_end, date_sozd__gte=date_start).count()


#################################################
##### Summa Sdelok                            ###
#################################################
                        sdelki_sum = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Да',
                                                               date_zakr__lte= date_end, date_zakr__gte=date_start)
                        sum=0
                        for i in sdelki_sum:
                            if i.reelt1 ==  user.username:
                                sum = sum+((i.komisia/2)*i.rielt_proc1/100)*2
                            if i.reelt2 ==  user.username:
                                sum = sum+((i.komisia/2)*i.rielt_proc2/100)*2
                            if i.reelt3 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc3/100)*2
                            if i.reelt4 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc4/100)*2
                            if i.reelt5 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc5/100)*2
                            if i.reelt6 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc6/100)*2
                            if i.reelt7 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc7/100)*2
                            if i.reelt8 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc8/100)*2
                            if i.reelt9 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc9/100)*2
                            if i.reelt10 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc10/100)*2

                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name, sdelok_calc=sdelki_count,
                                               sdelok_sum= sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
 ##########################
 # all For Sochi
 #########################
    zero_bal = reyting_po_sdelkam.objects.filter( sdelok_sum =0,).exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
    udl_bal  = reyting_po_sdelkam.objects.filter( sdelok_sum__lte = 80000, sdelok_sum__gt=1).order_by('-sdelok_sum').exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000, sdelok_sum__gt=80000).order_by('-sdelok_sum').exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter( sdelok_sum__gt=120000).order_by('-sdelok_sum').exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
 ###########################
 # all For Adler
 ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter( sdelok_sum =0, auth_group__in=['Офис в Адлере','Администрация Адлер'] )
    Audl_bal  = reyting_po_sdelkam.objects.filter( sdelok_sum__lte = 80000, sdelok_sum__gt=1,auth_group__in=['Офис в Адлере','Администрация Адлер'] ).order_by('-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000, sdelok_sum__gt=80000,auth_group__in=['Офис в Адлере','Администрация Адлер'] ).order_by('-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter( sdelok_sum__gt=120000, auth_group__in=['Офис в Адлере','Администрация Адлер'] ).order_by('-sdelok_sum')
##########################
# reiting in otdel for nach otdel
#########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000, sdelok_sum__gt=80000, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000, auth_group=gr).order_by('-sdelok_sum')
##########################
# reiting in otdel for Golovin
#########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел'or i.name == '2 Отдел'or i.name == '3 Отдел'or i.name == '4 Отдел':
            if i.name=='Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum)+int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                if str(sum) == 'None':
                    sum = 0
                s = reyt_sdelka_otd(otd = i.name, kommisia = sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    logout(request)
    return redirect('crm:login')




#############################
#News
############################

@login_required
def new_index_view(request):
    n1='Новости'
    n2='просмотр'
    n3 = zayavka.objects.filter(status='Свободен').count()
    post=news.objects.order_by('-datep')
    return render(request, 'crm/news/news_index.html', {'tppost':post,'tn1':n1,'tn2':n2, 'tn3':n3})

@login_required
def news_detail_view(request,idd):
    postnews=get_object_or_404(news, pk=idd)
    return render(request, 'crm/news/news_detail.html', {'tpnewsdetail':postnews})

@login_required
def news_edit_view(request,idd):
    n1='Новости'
    n2='редакция'
    post = get_object_or_404(news, pk=idd)
    if request.POST:
        newspostform = newsform(request.POST, instance=post)
        if newspostform.is_valid():
            newsform.save(newspostform)
            return redirect('crm:news_index')
    else:
        newspostform=newsform(instance=post)
    return render(request, 'crm/news/newsedit.html', {'tpnewspostform': newspostform,'tn1':n1,'tn2':n2})

@login_required
def news_postform(request):
    n1='Новости'
    n2='подача'
    if request.POST:
        form=newsform(request.POST)
        if form.is_valid():
            news=form.save(commit=False)
            news.autor=request.user
            news.datep = timezone.now()
            news.save()
            return redirect('crm:news_index')
    else:
        form=newsform()
    return render(request, 'crm/news/newsedit.html', {'tpnewspostform': form,'tn1':n1,'tn2':n2})

#####################
#Flats
########################

@login_required
def flat_postForm(request):
    n1='Квартиры'
    n2='подача на Cайт, RegionalRealty, ДомКлик, Росриэлт, Yandex'
    n3 = zayavka.objects.filter(status='Свободен').count()
    if request.POST:
        if request.user.userprofile1.ya == 'Да':
            form=yandex_flatform(request.POST)
        else:
            if request.user.groups.get().name =='Офис-менеджер':
                form = resep_flatform(request.POST)
               #form = flatform(request.POST)
            else:
                form = flatform(request.POST)
        if form.is_valid():
            #cena=form.cleaned_data['cena_sobstv']
            flat_obj=form.save(commit=False)
            flat_obj.author=request.user
            if request.user.groups.get().name == 'Офис-менеджер':
                flat_obj.domclick = 'Нет'
                flat_obj.ploshad = 0
                flat_obj.date_vigr_sait = timezone.datetime.now()
                flat_obj.cena_sobstv = 0
            else:
                flat_obj.domclick='Да'
            flat_obj.text_err ='False'
            flat_obj.dom_err = 'False'
            flat_obj.kv_err = 'False'
            flat_obj.date_sozd = timezone.datetime.now()
            flat_obj.date_vigr_sait = timezone.datetime.now()
            flat_obj.type = 'flat'
            flat_obj.save()
            return redirect('crm:newFlatgal', idd=flat_obj.pk)

    else:
        if request.user.userprofile1.ya == 'Да':
            form = yandex_flatform()
        else:
            if request.user.groups.get().name =='Офис-менеджер':
                form = resep_flatform()
            else:
                form = flatform()
    return render(request, 'crm/flat/flatedit.html', {'tpflatpostform': form,'tn1':n1,'tn2':n2,'tn3':n3})

@login_required
def flat_apparts_postForm(request):
    n1='Апартаменты'
    n2='подача на Cайт, RegionalRealty, ДомКлик, Росриэлт, Yandex'
    n3 = zayavka.objects.filter(status='Свободен').count()
    if request.POST:
        if request.user.userprofile1.ya == 'Да':
            form=flatform_appart(request.POST)
        else:
            if request.user.groups.get().name =='Офис-менеджер':
                form = resep_flatform(request.POST)
               #form = flatform(request.POST)
            else:
                form = flatform_appart(request.POST)
        if form.is_valid():
            #cena=form.cleaned_data['cena_sobstv']
            flat_obj=form.save(commit=False)
            flat_obj.author=request.user
            if request.user.groups.get().name == 'Офис-менеджер':
                flat_obj.domclick = 'Нет'
                flat_obj.ploshad = 0
                flat_obj.date_vigr_sait = timezone.datetime.now()
                flat_obj.cena_sobstv = 0
            else:
                flat_obj.domclick='Да'
            flat_obj.text_err ='False'
            flat_obj.dom_err = 'False'
            flat_obj.kv_err = 'False'
            flat_obj.date_sozd = timezone.datetime.now()
            flat_obj.date_vigr_sait = timezone.datetime.now()
            flat_obj.appart_pr = 'Да'
            flat_obj.status_gilya ='Нежилое помещение'
            flat_obj.type = 'flat'
            flat_obj.save()
            return redirect('crm:newFlatgal', idd=flat_obj.pk)

    else:
        if request.user.userprofile1.ya == 'Да':
            form = flatform_appart()
        else:
            if request.user.groups.get().name =='Офис-менеджер':
                form = resep_flatform()
            else:
                form = flatform_appart()
    return render(request, 'crm/flat/flatedit.html', {'tpflatpostform': form,'tn1':n1,'tn2':n2,'tn3':n3})

@login_required
def my_flatview_edit(request,idd):
    n1='Квартиры'
    n2='редакция'
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    post = get_object_or_404(flat_obj, pk=idd)
    if request.POST:
        if request.user.userprofile1.ya=='Да':
            flat=yandex_flateditform(request.POST, instance=post)
        else:
            flat = flateditform(request.POST, instance=post)
        if flat.is_valid():
            flat.save()
            return redirect('crm:newFlatgal', idd=post.pk)
        else:
            return render(request,'crm/flat/flatedit.html', {'tpflatpostform': flat})
            #return redirect('crm:flat_edit', idd=post.pk)
    else:
        if request.user.userprofile1.ya == 'Да':
            flat=yandex_flateditform(instance=post)
        else:
            flat=flateditform(instance=post)
        return render(request, 'crm/flat/flatedit.html', {'tpflatpostform': flat,'tn1':n1,'tn2':n2, 'tn3':n3,'t_my_ya_obj':my_ya_obj
                                                        , 'tcrm_obj_week_count': crm_obj_week_count,})

def flat_photo_new_view(request, idd):
    n1 = 'Редактировать фото'
    n2 = 'Фото'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    if request.POST:
        files = request.FILES.getlist('myfiles')
        for a_file in files:
            instance = flat_obj_gal(
                id_gal_id=idd,
                npict=a_file
            )
            instance.save()
        return redirect('crm:newFlatgal', idd=idd)#flat_obj_gal.id_gal_id)
    else:
        form = flat_pict_form()
        sp = get_object_or_404(flat_obj, pk=idd)
    return render(request,'any/flatgalform.html',{'tpform':form, 'tn1':n1, 'tn2':n2,'post':sp, 'tn3':n3,'t_my_ya_obj':my_ya_obj
                                                    ,'tcrm_obj_week_count': crm_obj_week_count,})

@login_required
def flat_del_view(request, idd, sidd):
    n1 = 'Редактировать фото'
    n2 = 'Фото'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    spsubj = flat_obj_gal.objects.get(pk=sidd)
    spsubj.delete()
    sp = get_object_or_404(flat_obj, pk=idd)
    form = vigruzkaGaleryForm()
    return redirect('crm:newFlatgal', idd=sp.pk)

###################################################
###  start All Flat list
###################################################

@login_required
def my_flatview_pub(request):
    n3 = zayavka.objects.filter(status='Свободен').count()
    n1='Квартиры'
    n2='опубликованные'
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    auser = request.user
    if request.POST:
        aFlatSearch = flat_search_form(request.POST)
        if aFlatSearch.is_valid():
            minp = aFlatSearch.cleaned_data['search_minp']
            maxp = aFlatSearch.cleaned_data['search_maxp']
            minc = aFlatSearch.cleaned_data['search_minc']
            maxc = aFlatSearch.cleaned_data['search_maxc']
            raionc = aFlatSearch.cleaned_data['search_raion']
            id = request.user.pk
            us = get_object_or_404(UserProfile1, pk=id)
            us.search_raion = raionc
            us.search_minp = minp
            us.search_maxp = maxp
            us.search_minc = minc
            us.search_maxc = maxc
            us.save()
            if raionc =='Любой':
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc),
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               type = 'flat').order_by('-date_sozd')
            else:
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',raion=raionc,
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc),
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               type = 'flat').order_by('-date_sozd')
    else:
        id = request.user.pk
        us = get_object_or_404(UserProfile1, pk = id)
        minp = us.search_minp
        maxp = us.search_maxp
        minc = us.search_minc
        maxc = us.search_maxc
        raionc = us.search_raion
        aFlatSearch=flat_search_form(initial={'search_minp': us.search_minp, 'search_maxp': us.search_maxp,
                                              'search_minc': us.search_minc, 'search_maxc': us.search_maxc,
                                              'search_raion': us.search_raion})
        if raionc == 'Любой':
            flatlist = flat_obj.objects.filter(status_obj='Опубликован',
                                           cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc),
                                           ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                           type='flat').order_by('-date_sozd')
        else:
            flatlist = flat_obj.objects.filter(status_obj='Опубликован', raion=raionc,
                                           cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc),
                                           ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                           type='flat').order_by('-date_sozd')
        if request.user.groups.get().name == 'Офис-менеджер' :
            flatlist = flat_obj.objects.filter(kadastr_pr='Нет', kadastr='').order_by('-date_sozd')
    return render(request,'crm/flat/all_flat_index.html',{'tpflatlist':flatlist,'tpaFlatSearch':aFlatSearch,'tn1':n1,'tn2':n2, 'tn3':n3,
                                                          'tcrm_obj_week_count':crm_obj_week_count,'t_my_ya_obj':my_ya_obj})

###################################################
###  esnd All Flat list
###################################################
###################################################
###  start Ecxlusive Flat list
###################################################

@login_required
def excl_flatview_pub(request):
    n3 = zayavka.objects.filter(status='Свободен').count()
    n1='Квартиры'
    n2='экслюзивные права на продажу агенства'
    studia = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Студия').order_by('raion')
    studia_count = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Студия').count()
    oneflat = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Однокомнатная').order_by('raion')
    oneflat_count = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Однокомнатная').count()
    twoflat = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Двухкомнатная').order_by('raion')
    twoflat_count = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Двухкомнатная').count()
    treeflat = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Трехкомнатная').order_by('raion')
    treeflat_count = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Трехкомнатная').count()
    mnflat = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Многокомнатная').order_by('raion')
    mnflat_count = flat_obj.objects.filter(exclusiv= 'Да',komnat= 'Многокомнатная').count()
    return render(request,'crm/flat/excl_flat_index.html',{'tn1':n1,'tn2':n2, 'tn3':n3,'ts':studia,'tsc':studia_count,
                                                           'tof':oneflat,'tofc':oneflat_count,'ttwf':twoflat,'ttwfc':twoflat_count,
                                                           'ttr':treeflat,'ttrc':treeflat_count,'tmf':mnflat,'tmc':mnflat_count})

###################################################
###  esnd Exclusive Flat list
###################################################
###################################################
###  start My Flat list
###################################################

@login_required
def my_flatview_unpub(request):
    n1='Квартиры'
    n2='личные'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    auser = request.user
    if request.POST:
        aFlatSearch = flat_search_form(request.POST)
        if aFlatSearch.is_valid():
            minp = aFlatSearch.cleaned_data['search_minp']
            maxp = aFlatSearch.cleaned_data['search_maxp']
            minc = aFlatSearch.cleaned_data['search_minc']
            maxc = aFlatSearch.cleaned_data['search_maxc']
            raionc = aFlatSearch.cleaned_data['search_raion']
            id = request.user.pk
            us = get_object_or_404(UserProfile1, pk=id)
            us.search_raion = raionc
            us.search_minp = minp
            us.search_maxp = maxp
            us.search_minc = minc
            us.search_maxc = maxc
            us.save()
            if raionc == 'Любой':
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc),
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               type = 'flat').order_by('-date_sozd')
            else:
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',raion=raionc,
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc),
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               type = 'flat').order_by('-date_sozd')
    else:
        id = request.user.pk
        us = get_object_or_404(UserProfile1, pk = id)
        minp = us.search_minp
        maxp = us.search_maxp
        minc = us.search_minc
        maxc = us.search_maxc
        raionc = us.search_raion
        aFlatSearch=flat_search_form(initial={'search_minp': us.search_minp, 'search_maxp': us.search_maxp,
                                              'search_minc': us.search_minc, 'search_maxc': us.search_maxc,
                                              'search_raion': us.search_raion})
        if raionc == 'Любой':
            flatlist=flat_obj.objects.filter(author=auser, type ='flat',
                                         cena_agenstv__gte = int(minc), cena_agenstv__lte = int(maxc),
                                         ploshad__gte = int(minp), ploshad__lte = int(maxp),).order_by('-date_sozd',)
        else:
            flatlist=flat_obj.objects.filter(author=auser, type ='flat',
                                         cena_agenstv__gte = int(minc), cena_agenstv__lte = int(maxc),
                                         ploshad__gte = int(minp), ploshad__lte = int(maxp),).order_by('-date_sozd',)
    return render(request,'crm/flat/all_flat_index.html',{'tpflatlist':flatlist,'tpaFlatSearch':aFlatSearch,'tn1':n1,
                                                          'tcrm_obj_week_count':crm_obj_week_count,'tn2':n2, 'tn3':n3,'t_my_ya_obj':my_ya_obj})
###################################################
###  end My Flat list
###################################################

@login_required
def all_flatview_pub(request):
    n1='Квартиры'
    n2='опубликованные'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    auser = request.user
    if request.POST:
        aFlatSearch = flat_search_form(request.POST)
        if aFlatSearch.is_valid():
            #a = flat_search_form.cleaned_data['min_prais']
            minp = aFlatSearch.cleaned_data['min_ploshad']
            maxp = aFlatSearch.cleaned_data['max_ploshad']
            minc = aFlatSearch.cleaned_data['min_prais']
            maxc = aFlatSearch.cleaned_data['max_prais']
            raionc = aFlatSearch.cleaned_data['raion_search']
            flatlist = flat_obj.objects.filter(status_obj='Опубликован',raion=raionc, ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc)).order_by('-pk')
    else:
        aFlatSearch=flat_search_form()
        flatlist=flat_obj.objects.filter(author=auser,status_obj='Опубликован').order_by('-pk')
    return render(request,'crm/flat/all_flat_index.html',{'tpflatlist':flatlist,'tpaFlatSearch':aFlatSearch,'tn1':n1,'tn2':n2, 'tn3':n3,
                                                          'tcrm_obj_week_count':crm_obj_week_count, 't_my_ya_obj':my_ya_obj})

##################################################
###For Seo xml_viev for sait
##################################################
@login_required
def all_flatviewSeo_pub(request):
    n1='Квартиры'
    n2='опубликованные на сайте'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    auser = request.user
    if request.POST:
        aFlatSearch = flat_search_form(request.POST)
        if aFlatSearch.is_valid():
            minp = aFlatSearch.cleaned_data['search_minp']
            maxp = aFlatSearch.cleaned_data['search_maxp']
            minc = aFlatSearch.cleaned_data['search_minc']
            maxc = aFlatSearch.cleaned_data['search_maxc']
            raionc = aFlatSearch.cleaned_data['search_raion']
            id = request.user.pk
            us = get_object_or_404(UserProfile1, pk=id)
            us.search_raion = raionc
            us.search_minp = minp
            us.search_maxp = maxp
            us.search_minc = minc
            us.search_maxc = maxc
            us.save()
            if raionc =='Любой':
                flatlist = flat_obj.objects.filter(status_obj='Опубликован', ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc),nazv='', cena_agenstv__lte=int(maxc)).order_by('-pk')
            else:
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',raion=raionc, ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc),nazv='', cena_agenstv__lte=int(maxc)).order_by('-pk')
    else:
        id = request.user.pk
        us = get_object_or_404(UserProfile1, pk = id)
        minp = us.search_minp
        maxp = us.search_maxp
        minc = us.search_minc
        maxc = us.search_maxc
        raionc = us.search_raion
        aFlatSearch=flat_search_form(initial={'search_minp': us.search_minp, 'search_maxp': us.search_maxp,
                                              'search_minc': us.search_minc, 'search_maxc': us.search_maxc,
                                              'search_raion': us.search_raion})
        if raionc == 'Любой':
            flatlist = flat_obj.objects.filter(status_obj='Опубликован', ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               cena_agenstv__gte=int(minc),
                                               cena_agenstv__lte=int(maxc)).exclude(nazv='').order_by('-pk')
        else:
            flatlist = flat_obj.objects.filter(status_obj='Опубликован', raion=raionc, ploshad__gte=int(minp),
                                               ploshad__lte=int(maxp),
                                               cena_agenstv__gte=int(minc),
                                               cena_agenstv__lte=int(maxc)).exclude(nazv='').order_by('-pk')
    return render(request,'crm/flat/all_flat_index.html',{'tpflatlist':flatlist,'tpaFlatSearch':aFlatSearch,'tn1':n1,'tn2':n2, 'tn3':n3,
                                                          'tcrm_obj_week_count':crm_obj_week_count, 't_my_ya_obj':my_ya_obj})

@login_required
def all_flatviewSeo_unpub(request):
    n1='Квартиры'
    n2='Неопубликованные на сайте1'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    auser = request.user
    if request.POST:
        aFlatSearch = flat_search_form(request.POST)
        if aFlatSearch.is_valid():
            minp = aFlatSearch.cleaned_data['search_minp']
            maxp = aFlatSearch.cleaned_data['search_maxp']
            minc = aFlatSearch.cleaned_data['search_minc']
            maxc = aFlatSearch.cleaned_data['search_maxc']
            raionc = aFlatSearch.cleaned_data['search_raion']
            id = request.user.pk
            us = get_object_or_404(UserProfile1, pk=id)
            us.search_raion = raionc
            us.search_minp = minp
            us.search_maxp = maxp
            us.search_minc = minc
            us.search_maxc = maxc
            us.save()
            if raionc =='Любой':
                flatlist = flat_obj.objects.filter(status_obj='Опубликован', ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc),nazv='', cena_agenstv__lte=int(maxc)).order_by('-pk')
            else:
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',raion=raionc, ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc),nazv='', cena_agenstv__lte=int(maxc)).order_by('-pk')
    else:
        id = request.user.pk
        us = get_object_or_404(UserProfile1, pk = id)
        minp = us.search_minp
        maxp = us.search_maxp
        minc = us.search_minc
        maxc = us.search_maxc
        raionc = us.search_raion
        aFlatSearch=flat_search_form(initial={'search_minp': us.search_minp, 'search_maxp': us.search_maxp,
                                              'search_minc': us.search_minc, 'search_maxc': us.search_maxc,
                                              'search_raion': us.search_raion})
        if raionc == 'Любой':
            flatlist = flat_obj.objects.filter(status_obj='Опубликован',  nazv='',
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc)).order_by('-pk')
        else:
            flatlist = flat_obj.objects.filter(status_obj='Опубликован', raion=raionc, nazv='',
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc)).order_by('-pk')

    return render(request,'crm/flat/all_flat_index.html',{'tpflatlist':flatlist,'tpaFlatSearch':aFlatSearch,'tn1':n1,'tn2':n2, 'tn3':n3,
                                                          'tcrm_obj_week_count':crm_obj_week_count, 't_my_ya_obj':my_ya_obj,  })
@login_required
def seo_flat_pub(request, idd):
    n1='Квартиры'
    n2='Неопубликованные на сайте'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    pict = flat_obj_gal.objects.filter(id_gal_id=idd)
    c = flat_obj_gal.objects.filter(id_gal_id=idd).count()
    post = get_object_or_404(flat_obj, pk=idd)
    if request.POST:
        form = seo_pub_form(request.POST, instance=post)
        if form.is_valid():
            form.save()
            #post.adress_utf = post.adress.encode('unicode-escape')
            #a = form.save(commit=False)
            post.allias = pytils.translit.slugify(post.nazv)#(u"тест и еще раз тест")
            post.date_vigr_sait = timezone.datetime.now()
            post.save()
            aFlatSearch=flat_search_form()
            flatlist=flat_obj.objects.filter(status_obj='Опубликован').exclude(nazv='').order_by('-pk')
            return render(request, 'crm/flat/all_flat_index.html',
                      {'tpflatlist': flatlist, 'tpaFlatSearch': aFlatSearch, 'tn1': n1, 'tn2': n2, 'tn3': n3})
    else:
        form = seo_pub_form(instance=post)
        pict_pass =post.date_sozd
    return render(request, 'crm/flat/flatedit.html',{'tpflatpostform': form, 'tdate':pict_pass, 'tc':c, 'tpict':pict, 'tn1': n1, 'tn2': n2 })



#########################################
###End for Seo
########################################




#####################################
## For kadastr kadastr_form
#######################################
def kadastr_edit(request,idd):
    post = get_object_or_404(flat_obj, pk=idd)
    adress = 'Сочи ул. '+post.adress+' '+post.kvart_numb
    if request.POST:
        form = kadastr_form(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('crm:all_flatpub')
    else:
        form = kadastr_form(instance=post)
    return render(request, 'crm/flat/flatedit.html', {'tpflatpostform':form,'tadr':adress})
#####################################
## For kadastr kadastr_form
#######################################



@login_required
def myflatDetail(request, idd):
    n1='Квартиры'
    n2='подробно'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    flat=get_object_or_404(flat_obj, pk=idd)
    my_kl = clients.objects.filter(category='Квартиры', raion__contains=flat.raion, st_pub__contains='Только у себя', budg_do__gte=flat.cena_agenstv ).order_by('-date_sozd')
    otd_kl = clients.objects.filter(category='Квартиры', raion__contains=flat.raion, st_pub__contains='Видно в отделе', budg_do__gte=flat.cena_agenstv ).order_by('-date_sozd')
    all_kl = clients.objects.filter(category='Квартиры', raion__contains=flat.raion, st_pub__contains='Видно всем', budg_do__gte=flat.cena_agenstv ).order_by('-date_sozd')
    return render(request, 'crm/flat/detail.html', {'tpflat':flat,'tp_my_kl':my_kl,'tp_otd_kl':otd_kl,'tp_all_kl':all_kl,'tn1':n1,'tn2':n2, 'tn3':n3,'t_my_ya_obj':my_ya_obj})

@login_required
def vestum_pub_view(request, idd):
    n1='Квартиры'
    n2='публикация на Vestum'
    if request.POST:
        post = get_object_or_404(flat_obj, pk =idd)
        form = vestum_pub_form(request.POST)
        if form.is_valid():
            nazv = form.cleaned_data['nov_nazv']
            post.nov_nazv = nazv
            post.vestum_pub = 'Да'
            post.save()
            return redirect('crm:all_flatpub')
    else:
        post = get_object_or_404(flat_obj, pk =idd)
        form = vestum_pub_form(instance=post)
    return render(request,'crm/flat/flatedit.html',{'tpflatpostform':form, 'tn1':n1,'tn2':n2})

def vestum_All_pub_view(request):
    n1='Квартиры'
    n2='опубликованные на Vestum'
    if request.POST:
        aFlatSearch = flat_search_form(request.POST)
        if aFlatSearch.is_valid():
            minp = aFlatSearch.cleaned_data['search_minp']
            maxp = aFlatSearch.cleaned_data['search_maxp']
            minc = aFlatSearch.cleaned_data['search_minc']
            maxc = aFlatSearch.cleaned_data['search_maxc']
            raionc = aFlatSearch.cleaned_data['search_raion']
            id = request.user.pk
            us = get_object_or_404(UserProfile1, pk=id)
            us.search_raion = raionc
            us.search_minp = minp
            us.search_maxp = maxp
            us.search_minc = minc
            us.search_maxc = maxc
            us.save()
            if raionc =='Любой':
                flatlist = flat_obj.objects.filter(status_obj='Опубликован', ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc),nazv='', cena_agenstv__lte=int(maxc), author_id=request.user.id, vestum_pub='Да').order_by('-pk')
            else:
                flatlist = flat_obj.objects.filter(status_obj='Опубликован',raion=raionc, ploshad__gte=int(minp), ploshad__lte=int(maxp),
                        cena_agenstv__gte=int(minc),nazv='', cena_agenstv__lte=int(maxc), author_id=request.user.id, vestum_pub='Да').order_by('-pk')
    else:
        id = request.user.pk
        us = get_object_or_404(UserProfile1, pk = id)
        minp = us.search_minp
        maxp = us.search_maxp
        minc = us.search_minc
        maxc = us.search_maxc
        raionc = us.search_raion
        aFlatSearch=flat_search_form(initial={'search_minp': us.search_minp, 'search_maxp': us.search_maxp,
                                              'search_minc': us.search_minc, 'search_maxc': us.search_maxc,
                                              'search_raion': us.search_raion})
        if raionc == 'Любой':
            flatlist = flat_obj.objects.filter(status_obj='Опубликован',  nazv='',
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp), author_id=request.user.id, vestum_pub='Да',
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc)).order_by('-pk')
        else:
            flatlist = flat_obj.objects.filter(status_obj='Опубликован', raion=raionc, nazv='',author_id=request.user.id, vestum_pub='Да',
                                               ploshad__gte=int(minp), ploshad__lte=int(maxp),
                                               cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc)).order_by('-pk')

    #flatlist = flat_obj.objects.filter(author_id=request.user.id, vestum_pub='Да')
    return render(request,'crm/flat/all_flat_index.html', {'tpaFlatSearch':aFlatSearch,'tpflatlist':flatlist,'tn1':n1, 'tn2':n2 })

@login_required
def all_flat_serch(request):
    form=flat_search_form()
    return render(request,'crm/flat/flat_search.html',{'tpformsearc':form})


@login_required
def myflatPrint(request, idd):
    flat=get_object_or_404(flat_obj, pk=idd)
    return render(request, 'crm/flat/print.html', {'tpflat':flat})

#################################################################
##  Text for domclick
#################################################################
@login_required
def dmIndexView(request):
    n1='Домклик'
    n2='текст для продвижения'
    dm = domclickText.objects.all().order_by('-dates')
    return render(request,'any/domclick/index.html',{'tdm':dm, 'tn1': n1, 'tn2': n2 })

def newDMtextView(request):
    n1='Домклик'
    n2='Новый текст для продвижения'
    if request.POST:
        form = DmTextForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crm:dm_index')
    else:
        form = DmTextForm()
    return render(request,'any/domclick/new.html',{'tpform':form, 'tn1': n1, 'tn2': n2 })

def EditDMtextView(request, idd):
    n1='Домклик'
    n2='Новый текст для продвижения'
    if request.POST:
        form = DmTextForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crm:dm_index')
    else:
        post = get_object_or_404(domclickText, pk=idd)
        form = DmTextForm(instance=post)
    return render(request,'any/domclick/new.html',{'tpform':form, 'tn1': n1, 'tn2': n2 })



#################################################################
##  End text for domclick
#################################################################
###################################
#####Feeds Fake Flats
###################################
def cianfeedview1(request):
    date= datetime.now() - timedelta(days=10)
    #post = feed.objects.filter(pub='Да', date_sozd__gte=date).order_by('-date_sozd')[:600]
    cn = get_object_or_404(TmpCianCount, pk=1)
    tsochi = cn.sochi
    tadler = cn.adler
    count = feed.objects.filter(pub='Да', date_sozd__gte=date).exclude( author__groups__name='Офис в Адлере').count()
    post = feed.objects.filter(pub='Да', date_sozd__gte=date).exclude( author__groups__name='Офис в Адлере').order_by(
        '-date_sozd')[:tsochi]
    if count < tsochi:
        apost = feed.objects.filter(pub='Да', date_sozd__gte=date,  author__groups__name='Офис в Адлере').order_by(
            '-date_sozd')[:tadler+(tsochi-count)]
    else:
        apost = feed.objects.filter(pub='Да', date_sozd__gte=date,  author__groups__name='Офис в Адлере').order_by(
            '-date_sozd')[:tadler]
    gal = feed_gallery.objects.all()
    return render(request,'any/cian.html',{'tppost': post, 'atppost':apost, 'tpgal':gal}, content_type="text/xml")

###################################
#####Feeds Real Flats
###################################
def cianfeedview(request):
    post = flat_obj.objects.filter(type='flat').order_by('-date_sozd')[:700]
    gal = flat_obj_gal.objects.all()
    return render(request,'any/real_flats_cian.html',{'tppost': post, 'tpgal':gal}, content_type="text/xml")


def MegaRealfeedview(request):
    date1= datetime.now() - timedelta(days=10)
    date = datetime.now()
    post = feed.objects.filter(pub='Да').order_by('-date_sozd')[:700]
    gal = feed_gallery.objects.all()
    return render(request,'any/megareal.html',{'tppost': post, 'tpgal':gal, 'tdate':date}, content_type="text/xml")

#fordomclic
def domclickfeedview(request):
    count = flat_obj.objects.all().exclude(kadastr='').count()#*0.1)*2
    post = flat_obj.objects.filter(domclick_pub='Да',type = 'flat').exclude(kadastr='')#.order_by('-kadastr','-datep')[:count]
    doma = flat_obj.objects.filter(domclick='Да', type='house').order_by('-datep')
    gal = flat_obj_gal.objects.all()
    #post = flat_obj.objects.filter(domclick_pub='Да').order_by('-datep')
    #post = flat_obj.objects.order_by('-datep')

    #ручной ввод текста сео
    date = datetime.now()
    #dm = domclickText.objects.all().order_by('-dates')[0]
    # end of ручной ввод текста сео
    # auto ввод текста сео
    date1 = timezone.now().day
    dm = get_object_or_404(domclickText, day = int(date1))
    #dm = ''
    # end of autoручной ввод текста сео
    return render(request,'any/ndomclick.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tcount':count, 'tdom':doma, 'tdm':dm }, content_type="text/xml")

#for Vestum
def vestumfeedview(request):
    count = flat_obj.objects.all().exclude(kadastr='').count()#*0.1)*2
    #porydok = vestum_poryadok_feed.objects.all()[0]
    #if porydok.poryadok == 'ПоВозрастанию':
    #    post = flat_obj.objects.filter(type = 'flat', vestum_pub='Да', author__is_active=True).exclude(nov_nazv='').order_by('-pk')[:700]
    #else:
    #    post = flat_obj.objects.filter(type='flat',  vestum_pub='Да', author__is_active=True).exclude( nov_nazv='').order_by('pk')[:700]
    post = flat_obj.objects.filter(type='flat', vestum_pub='Да', author__is_active=True).exclude(nov_nazv='').order_by(
        '-pk')[:700]
    doma = flat_obj.objects.filter(type='house', author__is_active=True).order_by(
        '-pk')[:700]
    gal = flat_obj_gal.objects.all()
    #ручной ввод текста сео
    date = datetime.now()
    #dm = domclickText.objects.all().order_by('-dates')[0]
    # end of ручной ввод текста сео
    # auto ввод текста сео
    date1 = timezone.now().day
    dm = get_object_or_404(domclickText, day = int(date1))
    # end of autoручной ввод текста сео
    return render(request,'any/vestum.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tcount':count,'tdom':doma , 'tdm':dm }, content_type="text/xml")#'tp':porydok
    #return render(request,'any/vestum.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tcount':count, 'tdm':dm }, content_type="text/xml")

#for Vestum
def vestumfeedview300(request):
    count = flat_obj.objects.all().exclude(kadastr='').count()#*0.1)*2
    porydok = vestum_poryadok_feed.objects.all()[0]
    if porydok.poryadok == 'ПоВозрастанию':
        post = flat_obj.objects.filter(type = 'flat', author__is_active=True, kadastr='').order_by('-pk')[:300]
    else:
        post = flat_obj.objects.filter(type='flat', author__is_active=True, kadastr='').order_by('pk')[:300]
    gal = flat_obj_gal.objects.all()
    #ручной ввод текста сео
    date = datetime.now()
    #dm = domclickText.objects.all().order_by('-dates')[0]
    # end of ручной ввод текста сео
    # auto ввод текста сео
    date1 = timezone.now().day
   # dm = get_object_or_404(domclickText, day = int(date1))
    # end of autoручной ввод текста сео
    return render(request,'any/vestum.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tcount':count,'tp':porydok  }, content_type="text/xml")
    #return render(request,'any/vestum.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tcount':count, 'tdm':dm }, content_type="text/xml")

def vestumFeedViewHouses(request):
    date = datetime.now()
    doma = flat_obj.objects.filter(type = 'house').order_by('-pk')
    return render(request,'any/vestumHouses.html', {'tdate':date,'tdom':doma}, content_type="text/xml")

#forYandex
def YandexFeedview(request):
    post = flat_obj.objects.filter(domclick='Да', type='flat').order_by('-datep')#[:2]
    doma = flat_obj.objects.filter(domclick='Да', type='house').order_by('-datep')
    uchastoc = flat_obj.objects.filter(domclick='Да', type='uchastok').order_by('-datep')
    gal = flat_obj_gal.objects.all()
    #post = flat_obj.objects.filter(author.userprofile1.tel='' ).order_by('-datep')
    #post = flat_obj.objects.order_by('-datep')
    #ручной ввод текста сео
    date = datetime.now()
    #dm = domclickText.objects.all().order_by('-dates')[0]
    # end of ручной ввод текста сео
    # auto ввод текста сео
    date1 = timezone.now().day
    dm = get_object_or_404(domclickText, day = int(date1))
    #dm = '21312321'
    # end of autoручной ввод текста сео
    return render(request,'any/YandexFeed.html',{'tppost': post, 'tpgal':gal, 'tdate':date,
                                                 'tdom':doma, 'tdm':dm, 'tuchastoc':uchastoc }, content_type="text/xml")

#for Mail ru & ula
def MailRuFeedview(request):
    post = flat_obj.objects.filter( type='flat').order_by('-pk')
    doma = flat_obj.objects.filter( type='house').order_by('-pk')
    gal = flat_obj_gal.objects.all()
    #post = flat_obj.objects.filter(author.userprofile1.tel='' ).order_by('-datep')
    #post = flat_obj.objects.order_by('-datep')
    #ручной ввод текста сео
    date = datetime.now()
    #dm = domclickText.objects.all().order_by('-dates')[0]
    # end of ручной ввод текста сео
    # auto ввод текста сео
    date1 = timezone.now().day
    dm = get_object_or_404(domclickText, day = int(date1))
    #dm = '21312321'
    # end of autoручной ввод текста сео
    return render(request,'any/MailFeed.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tdom':doma, 'tdm':dm }, content_type="text/xml")

#forYandex
def GRFeedview(request):
    post = flat_obj.objects.filter(domclick='Да', type='flat').order_by('-datep')
    doma = flat_obj.objects.filter(domclick='Да', type='house').order_by('-datep')
    gal = flat_obj_gal.objects.all()
    #post = flat_obj.objects.filter(author.userprofile1.tel='' ).order_by('-datep')
    #post = flat_obj.objects.order_by('-datep')
    #ручной ввод текста сео
    date = datetime.now()
    #dm = domclickText.objects.all().order_by('-dates')[0]
    # end of ручной ввод текста сео
    # auto ввод текста сео
    date1 = timezone.now().day
    dm = get_object_or_404(domclickText, day = int(date1))
    #dm = '21312321'
    # end of autoручной ввод текста сео
    return render(request,'any/GRFeed.html',{'tppost': post, 'tpgal':gal, 'tdate':date, 'tdom':doma, 'tdm':dm }, content_type="text/xml")


#forSait
def sait_vigr_view(request):
    post = flat_obj.objects.filter(date_vigr_sait=timezone.datetime.now().date()).exclude(nazv='')
    return render(request,'any/SaitFeed.html',{'tpost':post}, content_type="text/xml")



#CLIents
@login_required
def new_client_view(request):
    n1='Клиенты'
    n2='подача'
    if request.POST:
        form=newclientform(request.POST)
        if form.is_valid():
            clients=form.save(commit=False)
            clients.date_sozd=timezone.now()
            clients.auth=request.user
            clients.save(form)
            return redirect('crm:own_clienws')
    else:
        form=newclientform()
    return render(request,'crm/clients/newclient.html',{'tpformclient':form,'tn1':n1,'tn2':n2})

@login_required
def edit_client_view(request, idd):
    n1='Клиенты'
    n2='редакция'
    cl=get_object_or_404(clients, pk=idd)
    if request.POST:

        form = client_edit_form( request.POST, instance=cl)
        if form.is_valid:
            old_name = cl.auth.last_name
            cl = form.save(commit=False)
            cl.auth_old=old_name
            cl.auth=request.user
            cl.otd=request.user.groups.get().name
            cl.save()
            return redirect('crm:all_clienws')
    else:
        form=client_edit_form(instance=cl)
    return render(request,'crm/clients/editclient.html',{'tpform':form,'tn1':n1,'tn2':n2})

@login_required
def own_clients_view(request):
    n1='Клиенты'
    n2='личные'
    auser=request.user
    vclients=clients.objects.order_by('-date_sozd').filter(auth=auser, st_pub__contains='Только у себя',closed='False')
    return render(request,'crm/clients/clients.html',{'tpvclients':vclients,'tn1':n1,'tn2':n2})

@login_required
def all_clients_view(request):
    n1='Клиенты'
    n2='агенства'
    vclients=clients.objects.order_by('-date_sozd').filter(st_pub__contains='Видно всем',closed='False')
    return render(request,'crm/clients/clients.html',{'tpvclients':vclients,'tn1':n1,'tn2':n2})

@login_required
def otd_clients_view(request):
    n1='Клиенты'
    n2='в отделе'
    auser=request.user.groups.get().name
    vclients=clients.objects.order_by('-date_sozd').filter(otd=auser, st_pub__contains='Видно в отделе',closed='False')
    return render(request,'crm/clients/clients.html',{'tpvclients':vclients,'tn1':n1,'tn2':n2})

@login_required
def cliend_detail_view(request, idd):
    n1='Клиенты'
    n2='подробно'
    client=get_object_or_404(clients,pk=idd)
    #s = client.category
    if client.category == 'Квартиры':
     pub_obj = flat_obj.objects.filter( status_obj__contains='Опубликован', cena_agenstv__lte=client.budg_do ).order_by('-datep')
     un_pub_obj = flat_obj.objects.filter( status_obj__contains='Не опубликован', cena_agenstv__lte=client.budg_do ).order_by('-datep')
     return render(request,'crm/clients/detail.html',{'tpclient':client, 'tp_pub_obj':pub_obj,'tp_unp_obj':un_pub_obj,'tn1':n1,'tn2':n2 })
    if client.category == 'Дома':
     pub_obj = doma.objects.filter(status_obj__contains='Опубликован', cena_agenstv__lte=client.budg_do ).order_by('-date_sozd')
     un_pub_obj = doma.objects.filter(status_obj__contains='Не опубликован', cena_agenstv__lte=client.budg_do,author=request.user ).order_by('-date_sozd')
     return render(request,'crm/clients/detail.html',{'tpclient':client, 'tp_pub_obj':pub_obj,'tp_unp_obj':un_pub_obj,'tn1':n1,'tn2':n2 })
    if client.category == 'Участки':
     pub_obj = uchastok.objects.filter(status_obj__contains='Опубликован', cena_agenstv__lte=client.budg_do ).order_by('-date_sozd')
     un_pub_obj = uchastok.objects.filter( status_obj__contains='Не опубликован', cena_agenstv__lte=client.budg_do ).order_by('-date_sozd')
     return render(request,'crm/clients/detail.html',{'tpclient':client, 'tp_pub_obj':pub_obj,'tp_unp_obj':un_pub_obj,'tn1':n1,'tn2':n2 })




#####################
#Doma
#######################

@login_required
def new_dom_view(request):
    n1='Дома'
    n2='подача подача на Cайт, RegionalRealty, и Yandex недвижимость'
    if request.POST:
        form = doma_new_post(request.POST)
        if form.is_valid():
            flat_obj=form.save(commit=False)
            flat_obj.author=request.user
            flat_obj.domclick='Да'
            flat_obj.text_err ='False'
            flat_obj.dom_err = 'False'
            flat_obj.kv_err = 'False'
            flat_obj.date_vigr_sait = timezone.datetime.now()
            flat_obj.date_sozd = timezone.datetime.now()
            flat_obj.type = 'house'
            flat_obj.save()
            return redirect('crm:newFlatgal',  idd=flat_obj.pk)
    else:
        form=doma_new_post()
    return render(request,'crm/doma/new_dom.html',{'tpform':form,'tn1':n1,'tn2':n2 })

def domaeditview(request,idd):
    n1='Дома'
    n2='редакция'
    domform= get_object_or_404(flat_obj, pk = idd)
    if request.POST:
        form = doma_edit_form(request.POST, instance=domform)
        if form.is_valid():
            form.save()
            return redirect('crm:newFlatgal',  idd=domform.pk)
    else:
        form=doma_edit_form(instance=domform)
    return render(request,'crm/doma/new_dom.html',{'tpform':form,'tn1':n1,'tn2':n2 })

#############################################################################
#### Start of My Houses
#############################################################################
@login_required
def mu_unpob_doma_view(request):
    n1='Дома'
    n2='личное'
    if request.POST:
        form=flat_search_form(request.POST)
        if form.is_valid():
            minp=form.cleaned_data['search_minp']
            maxp=form.cleaned_data['search_maxp']
            minc=form.cleaned_data['search_minc']
            maxc=form.cleaned_data['search_maxc']
            raion_d=form.cleaned_data['search_raion']
            if raion_d =='Любой':
                doms=flat_obj.objects.filter(status_obj='Опубликован',type='house',
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),author_id=request.user.id,
                                       cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/doma/index_dom.html',{'tpform':form,'tpdoms':doms,'tn1':n1,'tn2':n2})
            else:
                doms=flat_obj.objects.filter(status_obj='Опубликован',type='house', raion=raion_d,
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),author_id=request.user.id,
                                       cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/doma/index_dom.html',{'tpform':form,'tpdoms':doms,'tn1':n1,'tn2':n2})
            #doms=flat_obj.objects.filter(raion=raion_d, ploshad__gte=int(minp), ploshad__lte=int(maxp),
            #                         type='house',cena_agenstv__gte=int(minc), cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
            #return render(request, 'crm/doma/index_dom.html', {'tpdoms': doms, 'tpform': form })
    else:
        form=flat_search_form()
        doms=flat_obj.objects.filter(author=request.user, type='house').order_by('-date_sozd')
        return render(request,'crm/doma/index_dom.html',{'tpdoms':doms, 'tpform':form,'tn1':n1,'tn2':n2 })
#############################################################################
#### end of My Houses
#############################################################################


#############################################################################
#### Start of All Houses
#############################################################################
@login_required
def mu_pob_doma_view(request):
    n1='Дома'
    n2='опубликованные'
    if request.POST:
        form = flat_search_form(request.POST)
        if form.is_valid():
            minp=form.cleaned_data['search_minp']
            maxp=form.cleaned_data['search_maxp']
            minc=form.cleaned_data['search_minc']
            maxc=form.cleaned_data['search_maxc']
            raion_d=form.cleaned_data['search_raion']
            if raion_d =='Любой':
                doms=flat_obj.objects.filter(status_obj='Опубликован',type='house',
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),
                                       cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/doma/index_dom.html',{'tpform':form,'tpdoms':doms,'tn1':n1,'tn2':n2})
            else:
                doms=flat_obj.objects.filter(status_obj='Опубликован',type='house', raion=raion_d,
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),
                                       cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/doma/index_dom.html',{'tpform':form,'tpdoms':doms,'tn1':n1,'tn2':n2})
    else:
        form = flat_search_form()
        doms = flat_obj.objects.filter(type='house').order_by('-date_sozd')
        return render(request, 'crm/doma/index_dom.html', {'tpdoms': doms, 'tpform':form,'tn1':n1,'tn2':n2})
#############################################################################
#### End of All Houses
#############################################################################
@login_required
def dom_detail_view(request, idd):
    n1='Дома'
    n2='подробно'
    dom=get_object_or_404(flat_obj, pk=idd)
    my_kl=clients.objects.filter(category='Дома',raion__contains=dom.raion,st_pub__contains='Только у себя',budg_do__gte=dom.cena_agenstv, ).order_by('-date_sozd')
    otd_kl = clients.objects.filter(category='Дома', raion__contains=dom.raion, st_pub__contains='Видно в отделе',budg_do__gte=dom.cena_agenstv, ).order_by('-date_sozd')
    all_kl = clients.objects.filter(category='Дома', raion__contains=dom.raion, st_pub__contains='Видно всем', budg_do__gte=dom.cena_agenstv, ).order_by('-date_sozd')
    return render(request,'crm/doma/detail.html',{'tpdom':dom,'tp_my_kl':my_kl,'tp_otd_kl':otd_kl,'tp_all_kl':all_kl,'tn1':n1,'tn2':n2})

@login_required
def dom_print_view(request, idd):
    dom=get_object_or_404(doma, pk=idd)
    return render(request,'crm/doma/print.html',{'tpdom':dom})

################
#UChastki
################

@login_required()
def new_uc_view(request):
    n1='Участки'
    n2='подача'
    if request.POST:
        form=uc_new_post(request.POST)
        if form.is_valid():
            flat_obj = form.save(commit=False)
            flat_obj.date_sozd = timezone.datetime.now()
            flat_obj.date_vigr_sait = timezone.datetime.now()
            flat_obj.ploshad = 0
            flat_obj.author = request.user
            flat_obj.type = 'uchastok'
            flat_obj.domclick = 'Да'
            flat_obj.save()
            #return redirect('crm:uc_detail', idd=flat_obj.pk)
            return redirect('crm:newFlatgal', idd=flat_obj.pk)
    else:
        form=uc_new_post()
    return render(request,'crm/uchastok/new_uch.html',{'tpform':form,'tn1':n1,'tn2':n2})

def ucheditview(request,idd):
    n1='Участки'
    n2='редакция'
    form =  get_object_or_404(flat_obj, pk = idd)
    id_uch=idd
    if request.POST:
        form = uc_edit_form(request.POST, instance=form)
        if form.is_valid():
            form.save()
            #return redirect('crm:uc_detail', idd=id_uch)
            return redirect('crm:newFlatgal', idd=idd)
    else:
        form=uc_edit_form(instance=form)
    return render(request,'crm/uchastok/new_uch.html',{'tpform':form,'tn1':n1,'tn2':n2})

@login_required
def pup_uchastki(request):
    n1='Участки'
    n2='В агенстве'
    if request.POST:
        form=flat_search_form(request.POST)
        if form.is_valid():
            minp=form.cleaned_data['search_minp']
            maxp=form.cleaned_data['search_maxp']
            minc=form.cleaned_data['search_minc']
            maxc=form.cleaned_data['search_maxc']
            raion_d=form.cleaned_data['search_raion']
            if raion_d =='Любой':
                uc=flat_obj.objects.filter(status_obj='Опубликован',type='uchastok',
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),  cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/uchastok/index.html',{'tpform':form,'tp_uch':uc,'tn1':n1,'tn2':n2})
            else:
                uc=flat_obj.objects.filter(status_obj='Опубликован',type='uchastok', raion=raion_d,
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),  cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/uchastok/index.html',{'tpform':form,'tp_uch':uc,'tn1':n1,'tn2':n2})
    else:
        form = flat_search_form()
        uc = flat_obj.objects.filter(status_obj='Опубликован',type='uchastok').order_by('-date_sozd')
        return render(request,'crm/uchastok/index.html',{'tpform':form,'tp_uch':uc,'tn1':n1,'tn2':n2})

@login_required
def unpup_uchastki(request):
    n1='Участки'
    n2='личное'
    if request.POST:
        form=flat_search_form(request.POST)
        if form.is_valid():
            minp=form.cleaned_data['search_minp']
            maxp=form.cleaned_data['search_maxp']
            minc=form.cleaned_data['search_minc']
            maxc=form.cleaned_data['search_maxc']
            raion_d=form.cleaned_data['search_raion']
            if raion_d =='Любой':
                uc=flat_obj.objects.filter(status_obj='Опубликован',type='uchastok',
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),author_id=request.user.id,
                                       cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/uchastok/index.html',{'tpform':form,'tp_uch':uc,'tn1':n1,'tn2':n2})
            else:
                uc=flat_obj.objects.filter(status_obj='Опубликован',type='uchastok', raion=raion_d,
                                       h_ploshad_uch__gte=int(minp),
                                       h_ploshad_uch__lte=int(maxp),author_id=request.user.id,
                                       cena_agenstv__gte=int(minc),
                                       cena_agenstv__lte=int(maxc)).order_by('-date_sozd')
                return render(request,'crm/uchastok/index.html',{'tpform':form,'tp_uch':uc,'tn1':n1,'tn2':n2})
    else:
        form = flat_search_form()
        uc=flat_obj.objects.filter(author=request.user, type='uchastok').order_by('-date_sozd')
        return render(request,'crm/uchastok/index.html',{'tp_uch':uc, 'tpform':form,'tn1':n1,'tn2':n2})

@login_required
def uch_detail_view(request, idd):
    n1='Участки'
    n2='подробно'
    auser = request.user.groups.get().name
    uc=get_object_or_404(flat_obj, pk=idd)
    my_kl=clients.objects.filter(auth=request.user, category='Участки',raion__contains=uc.raion,st_pub__contains='Только у себя',budg_do__gte=uc.cena_agenstv, ).order_by('-date_sozd')
    otd_kl = clients.objects.filter(category='Участки', raion__contains=uc.raion, st_pub__contains='Видно в отделе',budg_do__gte=uc.cena_agenstv, ).order_by('-date_sozd')
    all_kl = clients.objects.filter(category='Участки', raion__contains=uc.raion, st_pub__contains='Видно всем', budg_do__gte=uc.cena_agenstv, ).order_by('-date_sozd')
    return render(request,'crm/uchastok/detail.html',{'tp_uch':uc,'tp_my_kl':my_kl,'tp_otd_kl':otd_kl,'tp_all_kl':all_kl,'tn1':n1,'tn2':n2})

@login_required
def uch_print_view(request, idd):
    uc=get_object_or_404(uchastok, pk=idd)
    return render(request,'crm/uchastok/print.html',{'tp_uch':uc})

###################
###otchet po sdelke
####################

@login_required
def tempFioView(request):
    for i in otchet_nov.objects.all():
        s1 = ''
        if str(i.reelt1):
            n = str(i.reelt1)
            name = get_object_or_404(User, Q(username = n))
            s1 = s1 + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt2:
            n1 = str(i.reelt2)
            name = get_object_or_404(User, Q(username=n1))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt3:
            name = get_object_or_404(User, Q(username=i.reelt3))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt4:
            name = get_object_or_404(User, Q(username=i.reelt4))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt5:
            name = get_object_or_404(User, Q(username=i.reelt5))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt6:
            name = get_object_or_404(User, Q(username=i.reelt6))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt7:
            name = get_object_or_404(User, Q(username=i.reelt7))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt8:
            name = get_object_or_404(User, Q(username=i.reelt8))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt9:
            name = get_object_or_404(User, Q(username=i.reelt9))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        if i.reelt10:
            name = get_object_or_404(User, Q(username=i.reelt10))
            s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
        i.all_rielts = s1
        i.save()
    return redirect('crm:news')

@login_required
def new_otchet_view_All(request):
    n1='Отчет по сделке'
    n2='подача'
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    save = 'Сохранить и отправить отчет по сделке'
    if request.POST:
        otchetFormAllF = otchet_all_form(request.POST)
        if otchetFormAllF.is_valid():
            otchet_nov = otchetFormAllF.save(commit=False)
            s1=''
            if otchet_nov.reelt1:
                name = get_object_or_404(User, username = otchet_nov.reelt1)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 =s1+adl_pr+str(name.first_name)+' '+str(name.last_name)+' '
            if otchet_nov.reelt2:
                name = get_object_or_404(User, username = otchet_nov.reelt2)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt3:
                name = get_object_or_404(User, username = otchet_nov.reelt3)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt4:
                name = get_object_or_404(User, username = otchet_nov.reelt4)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt5:
                name = get_object_or_404(User, username = otchet_nov.reelt5)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt6:
                name = get_object_or_404(User, username = otchet_nov.reelt6)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt7:
                name = get_object_or_404(User, username = otchet_nov.reelt7)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt8:
                name = get_object_or_404(User, username = otchet_nov.reelt8)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt9:
                name = get_object_or_404(User, username = otchet_nov.reelt9)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+adl_pr+str(name.first_name)+' '+str(name.last_name)
            if otchet_nov.reelt10:
                name = get_object_or_404(User, username = otchet_nov.reelt10)
                if str(name.groups.get().name).__contains__('Адлер'):
                    adl_pr = '(Aдл)'
                else:
                    adl_pr = ''
                s1 = s1+'; '+str(name.first_name)+' '+str(name.last_name)

            if otchet_nov.reelt1:
                u_id = User.objects.get(username=otchet_nov.reelt1).groups.get().name
                if u_id:
                    otchet_nov.otd_reelt1 = str(u_id)
            if otchet_nov.reelt2:
                u_id2 = User.objects.get(username=otchet_nov.reelt2).groups.get().name
                if u_id2:
                    otchet_nov.otd_reelt2 = str(u_id2)
            if otchet_nov.reelt3:
                u_id3 = User.objects.get(username=otchet_nov.reelt3).groups.get().name
                if u_id3:
                    otchet_nov.otd_reelt3 = str(u_id3)
            if otchet_nov.reelt4:
                u_id4 = User.objects.get(username=otchet_nov.reelt4).groups.get().name
                if u_id4:
                    otchet_nov.otd_reelt4 = str(u_id4)
            if otchet_nov.reelt5:
                u_id5 = User.objects.get(username=otchet_nov.reelt5).groups.get().name
                if u_id5:
                    otchet_nov.otd_reelt5 = str(u_id5)
            if otchet_nov.reelt6:
                u_id6 = User.objects.get(username=otchet_nov.reelt6).groups.get().name
                if u_id6:
                    otchet_nov.otd_reelt6 = str(u_id6)
            if otchet_nov.reelt7:
                u_id7 = User.objects.get(username=otchet_nov.reelt7).groups.get().name
                if u_id7:
                    otchet_nov.otd_reelt7 = str(u_id7)
            if otchet_nov.reelt8:
                u_id8 = User.objects.get(username=otchet_nov.reelt8).groups.get().name
                if u_id8:
                    otchet_nov.otd_reelt8 = str(u_id8)
            if otchet_nov.reelt9:
                u_id9 = User.objects.get(username=otchet_nov.reelt9).groups.get().name
                if u_id9:
                    otchet_nov.otd_reelt9 = str(u_id9)
            if otchet_nov.reelt10:
                u_id10 = User.objects.get(username=otchet_nov.reelt10).groups.get().name
                if u_id10:
                    otchet_nov.otd_reelt10 = str(u_id10)


            otchet_nov.rielt = request.user
            otchet_nov.all_rielts = s1
            otchet_nov.date_sozd = timezone.datetime.now()
            if otchet_nov.vneseno_komisii:
                otchet_nov.vneseno_komisii_date = timezone.datetime.now()
            otchet_nov.sdelka_zakrita = 'Нет'
            if request.user.groups.get().name=='Офис в Адлере':
                otchet_nov.adler_pr='Адлер'
            if request.user.groups.get().name=='Администрация Адлер':
                otchet_nov.adler_pr='Адлер'
            otchet_nov.save()
            fiok = str(otchet_nov.rielt.first_name)+' '+str(otchet_nov.rielt.last_name)

            ss='<strong>Название объекта: </strong>'+str(otchet_nov.nazv_nov)+'</br>ФИО: <strong>'+str(otchet_nov.fio_kl)+'</br></strong>Телефон клиента: <strong>'+str(
                otchet_nov.tel_kl)+'</strong></br>Площадь объекта: <strong>'+str(otchet_nov.ploshad)
            ss=ss+'</strong></br>Цена объекта:<strong>'+str(otchet_nov.stoimost)+'</strong></br>Ипотека:<strong>'+str(
                otchet_nov.ipoteka)+'</strong></br>Рассрочка:<strong>'+str(otchet_nov.rasrochka)
            ss = ss + '</strong></br>Комиссия:<strong>' + str(
                otchet_nov.komisia) +'</strong></br>Дата создания:<strong>' + str(otchet_nov.date_sozd)+'</strong></br>Дата закрытия:<strong>' + str(otchet_nov.date_zakr)+'</br><strong>Риелторы в сделке: </strong>'

            if otchet_nov.reelt1:
                name = get_object_or_404(User, username = otchet_nov.reelt1)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc1)+'%'
            if otchet_nov.reelt2:
                name = get_object_or_404(User, username = otchet_nov.reelt2)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc2)+'%'
            if otchet_nov.reelt3:
                name = get_object_or_404(User, username = otchet_nov.reelt3)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc3)+'%'
            if otchet_nov.reelt4:
                name = get_object_or_404(User, username = otchet_nov.reelt4)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc4)+'%'
            if otchet_nov.reelt5:
                name = get_object_or_404(User, username = otchet_nov.reelt5)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc5)+'%'
            if otchet_nov.reelt6:
                name = get_object_or_404(User, username = otchet_nov.reelt6)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc6)+'%'
            if otchet_nov.reelt7:
                name = get_object_or_404(User, username = otchet_nov.reelt7)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc7)+'%'
            if otchet_nov.reelt8:
                name = get_object_or_404(User, username = otchet_nov.reelt8)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc8)+'%'
            if otchet_nov.reelt9:
                name = get_object_or_404(User, username = otchet_nov.reelt9)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc9)+'%'
            if otchet_nov.reelt10:
                name = get_object_or_404(User, username = otchet_nov.reelt10)
                ss = ss+'</br>'+str(name.first_name)+' '+str(name.last_name)+' '+str(otchet_nov.rielt_proc10)+'%'
            send_mail(fiok+'(Отчет об открытой сделке)', ss, 'zhem-otchet@mail.ru', #['hamster197@mail.ru'], fail_silently=False, html_message=ss)
                      ['otchet-zhem@mail.ru'], fail_silently=False, html_message=ss)
            if request.user.groups.get().name=='Офис в Адлере' or request.user.groups.get().name=='Администрация Адлер':
                send_mail(fiok + '(Отчет об открытой сделке Адлер)', ss, 'zhem-otchet@mail.ru',
                          ['2376361@zhem-realty.ru'], fail_silently=False, html_message=ss)
            return redirect('crm:otch_all_reelt')
    else:
        otchetFormAllF = otchet_all_form()


    return render(request,'any/newotchet.html', {'tpotchformall':otchetFormAllF, 'tn1':n1, 'tn2':n2, 'tsave':save, 'tn3':n3,
                                                 'tcrm_obj_week_count':crm_obj_week_count,'t_my_ya_obj':my_ya_obj})


@login_required
def reeelt_otchet_all_view(request):
    n1 ='Отчеты '
    #n2 =request.user.groups.get().name
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n2 = 'Период'
    date = timezone.datetime.now()

    if request.POST:
        dform = all_otchet_filtr_form(request.POST)
        if dform.is_valid():
            ##ds =dform.cleaned_data['st_date']
            ##de =dform.cleaned_data['end_date']
            ##ds1 =  ds#fdate = '1' + '-' + str(timezone.datetime.now().month) + '-' + str(timezone.datetime.now().year)
            # de =timezone.datetime.now()
            ##de1 = de#str(timezone.datetime.now().day) + '-' + str(timezone.datetime.now().month) + '-' + str(
            ##form = all_otchet_filtr_form(initial={'st_date': ds, 'end_date': de})
                #timezone.datetime.now().year)
            mothf = dform.cleaned_data['month']
            yearf = dform.cleaned_data['year']
            form = all_otchet_filtr_form(initial={'month': mothf, 'year': yearf})
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'
            ds1 = yearf+'-'+mothf+'-'+'01'
            de1 =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year,int(mothf))[1])
            ds = yearf+'-'+mothf+'-'+'01'
            de =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year,int(mothf))[1])

    else:
        ds = fdate = str(timezone.datetime.now().year)+'-'+ str(timezone.datetime.now().month) + '-' + '01'
        #de =timezone.datetime.now()
        de = str(timezone.datetime.now().year)+'-'+str(timezone.datetime.now().month)+'-'+str(timezone.datetime.now().day)

        ds1 = fdate = '1'+'-'+ str(timezone.datetime.now().month) + '-' + str(timezone.datetime.now().year)
        #de =timezone.datetime.now()
        de1 = str(timezone.datetime.now().day)+'-'+str(timezone.datetime.now().month)+'-'+str(timezone.datetime.now().year)
        form = all_otchet_filtr_form()
    #form = all_otchet_filtr_form()

    if request.user.groups.get().name == 'Администрация':
        open_otchet = otchet_nov.objects.filter(sdelka_zakrita='Нет').order_by('-date_sozd','-pk')
        closet_otchet = otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да').order_by('-date_zakr')
        sriv_otchet = otchet_nov.objects.filter(sdelka_zakrita='Срыв',date_zakr__gte=ds,date_zakr__lte=de).order_by('-date_zakr')
        rasr_otchet = otchet_nov.objects.filter(sdelka_zakrita='Рассрочка').order_by('-date_zakr')

        open_otchet_sum = otchet_nov.objects.filter(sdelka_zakrita='Нет').order_by('-pk').count()
        closet_otchet_sum = otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да').order_by('-pk').count()
        sriv_otchet_sum = otchet_nov.objects.filter(sdelka_zakrita='Срыв',date_zakr__gte=ds,date_zakr__lte=de).order_by('-pk').count()
        rasr_otchet_sum = otchet_nov.objects.filter(sdelka_zakrita='Рассрочка').order_by('-pk').count()
######################################################################################################################
        razn_otch = otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да', ot_kuda_kl='Другое').count()
        razn_otch = razn_otch +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Другое').count())
        razn_otch = razn_otch+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Другое').count())
        razn_otch = str(razn_otch+(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Другое').count()))
######################################################################################################################
        Avito =otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да', ot_kuda_kl='Avito').count()
        Avito = Avito +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Avito').count())
        Avito = Avito+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Avito').count())
        Avito = str(Avito+(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Avito').count()))
######################################################################################################################
        AvitoTurbo =otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de,  sdelka_zakrita='Да', ot_kuda_kl='Avito Turbo').count()
        AvitoTurbo = AvitoTurbo +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Avito Turbo').count())
        AvitoTurbo = AvitoTurbo+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Avito Turbo').count())
        AvitoTurbo = str(AvitoTurbo+(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Avito Turbo').count()))
######################################################################################################################
        Cian =otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de,  sdelka_zakrita='Да', ot_kuda_kl='Vestum').count()
        Cian = Cian +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Vestum').count())
        Cian = Cian+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Vestum').count())
        Cian = str(Cian +(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Vestum').count()))
######################################################################################################################
        sait =otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de,  sdelka_zakrita='Да', ot_kuda_kl='Сайт компании').count()
        sait = sait +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Сайт компании').count())
        sait = sait+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Сайт компании').count())
        sait = str(sait +(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Сайт компании').count()))
######################################################################################################################
        rec =otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да', ot_kuda_kl='По рекомендации').count()
        rec = rec +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='По рекомендации').count())
        rec = rec+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='По рекомендации').count())
        rec = str(rec +(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='По рекомендации').count()))
######################################################################################################################
        domclick = otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                              ot_kuda_kl='Домклик(Сбер)').count()
        domclick = domclick +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Домклик(Сбер)').count())
        domclick = domclick+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Домклик(Сбер)').count())
        domclick = str(domclick +(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Домклик(Сбер)').count()))
######################################################################################################################
        Yandex = otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                              ot_kuda_kl='Yandex Недвижимость').count()
        Yandex = Yandex +(otchet_nov.objects.filter(date_sozd__gte=ds, date_sozd__lte=de, sdelka_zakrita='Рассрочка',
                                              ot_kuda_kl='Yandex Недвижимость').count())
        Yandex = Yandex+(otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Срыв',
                                              ot_kuda_kl='Yandex Недвижимость').count())
        Yandex = str(Yandex +(otchet_nov.objects.filter(sdelka_zakrita='Нет',  ot_kuda_kl='Yandex Недвижимость').count()))
######################################################################################################################
        sum =otchet_nov.objects.filter(date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да').aggregate(Sum("komisia"))
        sum_rasr1 = otchet_nov.objects.filter(vneseno_komisii_date__gte=ds, vneseno_komisii_date__lte=de,
                                              sdelka_zakrita='Рассрочка').aggregate(Sum("vneseno_komisii2"))
        sum_rasr2 = otchet_nov.objects.filter(vneseno_komisii_date2__gte=ds, vneseno_komisii_date2__lte=de,
                                              sdelka_zakrita='Рассрочка').aggregate(Sum("vneseno_komisii2"))
        sum_rasr3 = otchet_nov.objects.filter(vneseno_komisii_date3__gte=ds, vneseno_komisii_date3__lte=de,
                                              sdelka_zakrita='Рассрочка').aggregate(Sum("vneseno_komisii3"))
        sum_rasr4 = otchet_nov.objects.filter(vneseno_komisii_date4__gte=ds, vneseno_komisii_date4__lte=de,
                                              sdelka_zakrita='Рассрочка').aggregate(Sum("vneseno_komisii4"))
        sum_rasr5 = otchet_nov.objects.filter(vneseno_komisii_date5__gte=ds, vneseno_komisii_date5__lte=de,
                                              sdelka_zakrita='Рассрочка').aggregate(Sum("vneseno_komisii5"))
        #sum_adler = otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, adler_pr='Адлер',\
                                                #sdelka_zakrita = 'Да').aggregate(Sum("komisia"))
        grp = 'Адлер'
        sum_adler = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de,
                                             sdelka_zakrita = 'Да').aggregate(Sum("komisia"))
        sum_adler_rasr1 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date__gte=ds, vneseno_komisii_date__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii"))
        sum_adler_rasr2 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp), vneseno_komisii_date2__gte=ds, vneseno_komisii_date2__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii2"))
        sum_adler_rasr3 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date3__gte=ds, vneseno_komisii_date3__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii3"))
        sum_adler_rasr4 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date4__gte=ds, vneseno_komisii_date4__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii4"))
        sum_adler_rasr5 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date5__gte=ds, vneseno_komisii_date5__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii5"))

        grp = 'Отдел'
        sum_sochi = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de,
                                             sdelka_zakrita = 'Да').aggregate(Sum("komisia"))

        sum_sochi_rasr1 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date__gte=ds, vneseno_komisii_date__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii"))
        sum_sochi_rasr2 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp), vneseno_komisii_date2__gte=ds, vneseno_komisii_date2__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii2"))
        sum_sochi_rasr3 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date3__gte=ds, vneseno_komisii_date3__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii3"))
        sum_sochi_rasr4 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date4__gte=ds, vneseno_komisii_date4__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii4"))
        sum_sochi_rasr5 = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),vneseno_komisii_date5__gte=ds, vneseno_komisii_date5__lte=de,
                                             sdelka_zakrita = 'Рассрочка').aggregate(Sum("vneseno_komisii5"))
        #############################################################################
        ### For all Summ
        #############################################################################
        if sum.get('komisia__sum'):
            s_sochi_m=str(sum.get('komisia__sum')*45/100)
        else:
            s_sochi_m='0'

        if sum_rasr1.get('vneseno_komisii__sum'):
            s_sochi_m = s_sochi_m=str(float(s_sochi_m)+float(sum_rasr1.get('vneseno_komisii__sum')*45/100))
        else:
            s_sochi_m=s_sochi_m

        if sum_rasr2.get('vneseno_komisii2__sum'):
            s_sochi_m=str(float(s_sochi_m)+float(sum_rasr2.get('vneseno_komisii2__sum')*45/100))
        else:
            s_sochi_m=s_sochi_m

        if sum_rasr3.get('vneseno_komisii3__sum'):
            s_sochi_m=str(float(s_sochi_m)+float(sum_rasr3.get('vneseno_komisii3__sum')*45/100))
        else:
            s_sochi_m=s_sochi_m

        if sum_rasr4.get('vneseno_komisii__sum4'):
            s_sochi_m=str(float(s_sochi_m)+float(sum_rasr4.get('vneseno_komisii4__sum')*45/100))
        else:
            s_sochi_m=s_sochi_m

        if sum_rasr5.get('vneseno_komisii5__sum'):
            s_sochi_m=str(int(s_sochi_m)+int(sum_rasr5.get('vneseno_komisii5__sum')*45/100))
        else:
            s_sochi_m=s_sochi_m
        #############################################################################
        ### For SOchi Summ
        #############################################################################
        if sum_sochi.get('komisia__sum'):
            s_sochi=str(sum_sochi.get('komisia__sum')*45/100)
        else:
            s_sochi='0'

        if sum_sochi_rasr1.get('vneseno_komisii__sum'):
            s_sochi = s_sochi=str(float(s_sochi)+float(sum_sochi_rasr1.get('vneseno_komisii__sum')*45/100))
        else:
            s_sochi=s_sochi

        if sum_sochi_rasr2.get('vneseno_komisii2__sum'):
            s_sochi=str(float(s_sochi)+float(sum_sochi_rasr2.get('vneseno_komisii2__sum')*45/100))
        else:
            s_sochi=s_sochi

        if sum_sochi_rasr3.get('vneseno_komisii3__sum'):
            s_sochi=str(float(s_sochi)+float(sum_sochi_rasr3.get('vneseno_komisii3__sum')*45/100))
        else:
            s_sochi=s_sochi

        if sum_sochi_rasr4.get('vneseno_komisii4__sum'):
            s_sochi=str(float(s_sochi)+float(sum_sochi_rasr4.get('vneseno_komisii4__sum')*45/100))
        else:
            s_sochi=s_sochi

        if sum_sochi_rasr5.get('vneseno_komisii5__sum'):
            s_sochi=str(float(s_sochi)+float(sum_sochi_rasr1.get('vneseno_komisii5__sum')*45/100))
        else:
            s_sochi=s_sochi

        #############################################################################
        ### For Adler Summ
        #############################################################################
        if sum_adler.get('komisia__sum'):
            s_adler=str(sum_adler.get('komisia__sum')*45/100)
        else:
            s_adler='0'

        if sum_adler_rasr1.get('vneseno_komisii__sum'):
            s_adler=str(float(s_adler)+float(sum_adler_rasr1.get('vneseno_komisii__sum')*45/100))
        else:
            s_adler=s_adler

        if sum_adler_rasr2.get('vneseno_komisii2__sum'):
            s_adler=str(float(s_adler)+float(sum_adler_rasr2.get('vneseno_komisii2__sum')*45/100))
        else:
            s_adler=s_adler

        if sum_adler_rasr3.get('vneseno_komisii3__sum'):
            s_adler=str(float(s_adler)+float(sum_adler_rasr3.get('vneseno_komisii3__sum')*45/100))
        else:
            s_adler=s_adler

        if sum_adler_rasr4.get('vneseno_komisii4__sum'):
            s_adler=str(float(s_adler)+float(sum_adler_rasr4.get('vneseno_komisii4__sum')*45/100))
        else:
            s_adler=s_adler

        if sum_adler_rasr5.get('vneseno_komisii5__sum'):
            s_adler=str(float(s_adler)+float(sum_adler_rasr1.get('vneseno_komisii5__sum')*45/100))
        else:
            s_adler=s_adler



        n2 = n2 +' c '+str(ds1)+' по '+str(de1)+';  ' +'     '+'     '+' Прибыль компании: '+ s_sochi_m+';(Сочи: '\
             +s_sochi+'/Адлер: '+s_adler+')'
        group = request.user.groups.get().name

        return render(request,'any/reel_otchet_all.html', {'tn1':n1, 'tn2':n2, 'tn3':n3, 'tOpOtchet':open_otchet,'tClOtchet':closet_otchet, 'trazn':razn_otch, 'tavito':Avito,
                                                           'tAvitoTurbo':AvitoTurbo, 'tCian':Cian,'tsait':sait,'trec':rec, 'tpform':form, 'tgroup':group, 'tyandex':Yandex,
                                                           'tdomclick':domclick, 'tdate':date, 'tSRotchet':sriv_otchet, 'tRasrOtchet':rasr_otchet,
                                                           'topen_otchet_sum':open_otchet_sum,'tcloset_otchet_sum':closet_otchet_sum,'tsriv_otchet_sum':sriv_otchet_sum,
                                                           'trasr_otchet_sum':rasr_otchet_sum,'tde':date,'t_my_ya_obj':my_ya_obj})
    #if request.user.groups.get().name =='Администрация Адлер':
    #if request.user.UserProfile1.nach_otd == 'Да':
    if request.user.userprofile1.nach_otd == 'Да':
        if request.user.groups.get().name =='Администрация Адлер':
            grp = 'Адлер'#request.user.groups.get().name
        else:
            grp = request.user.groups.get().name
        open_otchet = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, sdelka_zakrita='Нет' ).order_by('-pk')
        closet_otchet = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да').order_by('-pk')
        sriv_otchet = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),sdelka_zakrita='Срыв', date_zakr__gte=ds, date_zakr__lte=de).order_by('-pk')
        rasr_otchet = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp), sdelka_zakrita='Рассрочка').order_by('-pk')

        open_otchet_sum = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, sdelka_zakrita='Нет').order_by('-pk').count()
        closet_otchet_sum = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita='Да').order_by('-pk').count()
        sriv_otchet_sum = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),sdelka_zakrita='Срыв', date_zakr__gte=ds, date_zakr__lte=de).order_by('-pk').count()
        rasr_otchet_sum = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),sdelka_zakrita='Рассрочка').order_by('-pk').count()

        razn_otch = str(
            otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                      ot_kuda_kl='Другое').count())
        Avito = str(
            otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                      ot_kuda_kl='Avito').count())
        AvitoTurbo = str(
            otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                      ot_kuda_kl='Avito Turbo').count())
        Cian = str(
            otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                      ot_kuda_kl='Cian').count())
        sait = str(
            otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                      ot_kuda_kl='Сайт компании').count())
        rec = str(otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                            ot_kuda_kl='По рекомендации').count())
        domclick = str(otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                              ot_kuda_kl='Домклик(Сбер)').count())
        Yandex = str(otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',
                                              ot_kuda_kl='Yandex Недвижимость').count())
        sum_adler = otchet_nov.objects.filter(Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
            | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(otd_reelt7__contains=grp)
            | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp),date_zakr__gte=ds, date_zakr__lte=de,
                                             sdelka_zakrita = 'Да').aggregate(Sum("komisia"))

        if sum_adler.get('komisia__sum'):
            s_adler=str(sum_adler.get('komisia__sum')*45/100)
        else:
            s_adler='0'

        n2 = n2 + '; c ' + str(ds1) + ' по ' + str(de1) + ' Кол-во сделок: ' + str(
            closet_otchet.count()) + ', Прибыль филиала: ' + s_adler
        group = request.user.groups.get().name
        return render(request,'any/reel_otchet_all.html', {'tn1':n1, 'tn2':n2, 'tn3':n3, 'tOpOtchet':open_otchet,'tClOtchet':closet_otchet, 'trazn':razn_otch, 'tavito':Avito, 'tSRotchet':sriv_otchet,
                                                           'tAvitoTurbo':AvitoTurbo,'tgroup':group, 'tCian':Cian,'tsait':sait,'trec':rec, 'tpform':form,
                                                           'tyandex':Yandex, 'tdomclick':domclick, 'tRasrOtchet':rasr_otchet,
                                                           'topen_otchet_sum': open_otchet_sum,'tcloset_otchet_sum': closet_otchet_sum,
                                                           'tsriv_otchet_sum': sriv_otchet_sum,'trasr_otchet_sum': rasr_otchet_sum,'tde':date,'t_my_ya_obj':my_ya_obj})
    else:
        open_otchet = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            date_zakr__gte=ds,sdelka_zakrita = 'Нет').order_by('-pk')
        closet_otchet = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita = 'Да').order_by('-pk')
        sriv_otchet = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            sdelka_zakrita='Срыв', date_zakr__gte=ds, date_zakr__lte=de).order_by('-pk')
        rasr_otchet = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            sdelka_zakrita='Рассрочка').order_by('-pk')

        open_otchet_sum = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            date_zakr__gte=ds, sdelka_zakrita = 'Нет').order_by('-pk').count()
        closet_otchet_sum = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            date_zakr__gte=ds,date_zakr__lte=de, sdelka_zakrita = 'Да').order_by('-pk').count()
        sriv_otchet_sum = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            sdelka_zakrita='Срыв', date_zakr__gte=ds, date_zakr__lte=de).order_by('-pk').count()
        rasr_otchet_sum = otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
            sdelka_zakrita='Рассрочка').order_by('-pk').count()

        razn_otch = str(
            otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                      ot_kuda_kl='Другое',).count())
        Avito = str(
            otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                      ot_kuda_kl='Avito',).count())
        AvitoTurbo = str(
            otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                      ot_kuda_kl='Avito Turbo',).count())
        Cian = str(
            otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                      ot_kuda_kl='Cian',).count())
        sait = str(
            otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                      ot_kuda_kl='Сайт компании',).count())
        rec = str(otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                                            date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                            ot_kuda_kl='По рекомендации',).count())

        domclick = str(otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                                            date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                            ot_kuda_kl='Домклик(Сбер)',).count())
        Yandex = str(otchet_nov.objects.filter(Q(reelt1=request.user) | Q(reelt2=request.user) | Q(reelt3=request.user)
            | Q(reelt4=request.user) | Q(reelt5=request.user) | Q(reelt6=request.user) | Q(reelt7=request.user)
            | Q(reelt8=request.user) | Q(reelt9=request.user) | Q(reelt10=request.user),
                                            date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita = 'Да',
                                            ot_kuda_kl='Yandex Недвижимость',).count())

        sum = otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, rielt=request.user,
                                        sdelka_zakrita='Да').aggregate(Sum("komisia"))
       # if sum.get('komisia__sum'):
       #     s=str(sum.get('komisia__sum'))
       # else:
       #     s='0'

        n2 = 'Агентский'
        n2 = n2 + '; c ' + str(ds1) + ' по ' + str(de1) + ' Кол-во сделок: ' + str(
            closet_otchet.count()) #+ ' Коммисия:' + s


        return render(request,'any/reel_otchet_all.html', {'tn1':n1, 'tn2':n2, 'tn3':n3, 'tOpOtchet':open_otchet,'tClOtchet':closet_otchet, 'trazn':razn_otch, 'tavito':Avito,
                                                           'tAvitoTurbo':AvitoTurbo, 'tCian':Cian,'tsait':sait,'trec':rec,'tyandex':Yandex,
                                                           'tdomclick':domclick,
                                                           'tpform':form, 'tSRotchet':sriv_otchet,
                                                           'tRasrOtchet': rasr_otchet,'topen_otchet_sum':open_otchet_sum,'tcloset_otchet_sum':closet_otchet_sum,'tsriv_otchet_sum':sriv_otchet_sum,
                                                           'trasr_otchet_sum':rasr_otchet_sum,'tde':date,'t_my_ya_obj':my_ya_obj,'tcrm_obj_week_count':crm_obj_week_count,})

@login_required
def reelt_sdelka_otchet_detail_view(request, idd):
    n1 ='Отчет по сделке'
    sdelka = get_object_or_404(otchet_nov, pk=idd)
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    n2 ='Стоимость: '+str(sdelka.stoimost)+ ' руб.; Комисия: '+str(sdelka.komisia)+' руб.'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    ostatok=sdelka.komisia-sdelka.vneseno_komisii-sdelka.vneseno_komisii2-sdelka.vneseno_komisii3-sdelka.vneseno_komisii4-sdelka.vneseno_komisii5
    if sdelka.reelt1:
        n11 = User.objects.get(username__exact=sdelka.reelt1).first_name+' '+User.objects.get(username__exact=sdelka.reelt1).last_name
        p11 = (sdelka.komisia/2)*sdelka.rielt_proc1/100
    else:
        n11 = ''
        p11 = ''
    if sdelka.reelt2:
        n22 = User.objects.get(username__exact=sdelka.reelt2).first_name+' '+User.objects.get(username__exact=sdelka.reelt2).last_name
        p22 = (sdelka.komisia / 2) * sdelka.rielt_proc2 / 100
    else:
        n22 = ''
        p22 = ''
    if sdelka.reelt3:
        n33 = User.objects.get(username__exact=sdelka.reelt3).first_name+' '+User.objects.get(username__exact=sdelka.reelt3).last_name
        p33 = (sdelka.komisia / 2) * sdelka.rielt_proc3 / 100
    else:
        n33 = ''
        p33 = ''
    if sdelka.reelt4:
        n44 = User.objects.get(username__exact=sdelka.reelt4).first_name+' '+User.objects.get(username__exact=sdelka.reelt4).last_name
        p44 = (sdelka.komisia / 2) * sdelka.rielt_proc4 / 100
    else:
        n44 = ''
        p44 = ''
    if sdelka.reelt5:
        n55 = User.objects.get(username__exact=sdelka.reelt5).first_name+' '+User.objects.get(username__exact=sdelka.reelt5).last_name
        p55 = (sdelka.komisia / 2) * sdelka.rielt_proc5 / 100
    else:
        n55 = ''
        p55 = ''
    if sdelka.reelt6:
        n66 = User.objects.get(username__exact=sdelka.reelt6).first_name+' '+User.objects.get(username__exact=sdelka.reelt6).last_name
        p66 = (sdelka.komisia / 2) * sdelka.rielt_proc6 / 100
    else:
        n66 = ''
        p66 = ''
    if sdelka.reelt7:
        n77 = User.objects.get(username__exact=sdelka.reelt7).first_name+' '+User.objects.get(username__exact=sdelka.reelt7).last_name
        p77 = (sdelka.komisia / 2) * sdelka.rielt_proc7 / 100
    else:
        n77 = ''
        p77 = ''
    if sdelka.reelt8:
        n88 = User.objects.get(username__exact=sdelka.reelt8).first_name+' '+User.objects.get(username__exact=sdelka.reelt8).last_name
        p88 = (sdelka.komisia / 2) * sdelka.rielt_proc8 / 100
    else:
        n88 = ''
        p88 = ''
    if sdelka.reelt9:
        n99 = User.objects.get(username__exact=sdelka.reelt9).first_name+' '+User.objects.get(username__exact=sdelka.reelt9).last_name
        p99 = (sdelka.komisia / 2) * sdelka.rielt_proc9 / 100
    else:
        n99 = ''
        p99 = ''
    if sdelka.reelt10:
        n10 = User.objects.get(username__exact=sdelka.reelt10).first_name+' '+User.objects.get(username__exact=sdelka.reelt10).last_name
        p10 = (sdelka.komisia / 2) * sdelka.rielt_proc10 / 100
    else:
        n10 = ''
        p10 = ''

    if request.user.username == 'golovind' or request.user.username == 'kondratovf':
        sdelka.pr_prosmotra_golovin = 'Да'
        sdelka.save()


    return render(request, 'any/reelt_otchet_detail.html', {'tsdelka': sdelka, 'tn1': n1, 'tn2': n2, 'tn3':n3,
                                                            'tn11': n11, 'tn22': n22, 'tn33': n33, 'tn44': n44,
                                                            'tn55': n55, 'tn66': n66, 'tn77': n77, 'tn88': n88,
                                                            'tn99': n99, 'tn10': n10,
                                                            'tpn11':p11, 'tpn22':p22, 'tpn33':p33, 'tpn44':p44,
                                                            'tpn55':p55,'tpn66':p66,'tpn77':p77,'tpn11':p11,
                                                            'tpn88': p88,'tpn99':p99,'tpn10':p10,'t_my_ya_obj':my_ya_obj,
                                                            'tcrm_obj_week_count':crm_obj_week_count,'tost':ostatok, })

def temp_otch_view(request):
    for p in otchet_nov.objects.all():
        if p.reelt1:
            u_id = User.objects.get(username=p.reelt1).groups.get().name
            if u_id:
                p.otd_reelt1 = str(u_id)
                #p.save()
        if p.reelt2:
            u_id2 = User.objects.get(username=p.reelt2).groups.get().name
            if u_id2:
                p.otd_reelt2 = str(u_id2)
        if p.reelt3:
            u_id3 = User.objects.get(username=p.reelt3).groups.get().name
            if u_id3:
                p.otd_reelt3 = str(u_id3)
        if p.reelt4:
            u_id4 = User.objects.get(username=p.reelt4).groups.get().name
            if u_id4:
                p.otd_reelt4 = str(u_id4)
        if p.reelt5:
            u_id5 = User.objects.get(username=p.reelt5).groups.get().name
            if u_id5:
                p.otd_reelt5 = str(u_id5)
        if p.reelt6:
            u_id6 = User.objects.get(username=p.reelt6).groups.get().name
            if u_id6:
                p.otd_reelt6 = str(u_id6)
        if p.reelt7:
            u_id7 = User.objects.get(username=p.reelt7).groups.get().name
            if u_id7:
                p.otd_reelt7 = str(u_id7)
        if p.reelt8:
            u_id8 = User.objects.get(username=p.reelt8).groups.get().name
            if u_id8:
                p.otd_reelt8 = str(u_id8)
        if p.reelt9:
            u_id9 = User.objects.get(username=p.reelt9).groups.get().name
            if u_id9:
                p.otd_reelt9 = str(u_id9)
        if p.reelt10:
            u_id10 = User.objects.get(username=p.reelt10).groups.get().name
            if u_id10:
                p.otd_reelt10 = str(u_id10)
        p.save()
    return redirect('crm:otch_all_reelt')


def otchet_edit_view(request, idd):
    n1 ='Отчет по сделке'
    n2 ='редакция'
    otchet = get_object_or_404(otchet_nov, pk = idd)
    sdelka = get_object_or_404(otchet_nov, pk = idd)
    group = request.user.groups.get().name
    if request.user.username == 'golovind' or request.user.username == 'kondratovf':
        sdelka.pr_prosmotra_golovin = 'Да'
        sdelka.save()
    if request.POST:
        form=otchet_all_form1(request.POST, instance=otchet)
        if form.is_valid():
            s1 = ''
            if otchet.reelt1:
                name = get_object_or_404(User, username=otchet.reelt1)
                s1 = s1 + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt2:
                name = get_object_or_404(User, username=otchet.reelt2)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt3:
                name = get_object_or_404(User, username=otchet.reelt3)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt4:
                name = get_object_or_404(User, username=otchet.reelt4)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt5:
                name = get_object_or_404(User, username=otchet.reelt5)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt6:
                name = get_object_or_404(User, username=otchet.reelt6)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt7:
                name = get_object_or_404(User, username=otchet.reelt7)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt8:
                name = get_object_or_404(User, username=otchet.reelt8)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt9:
                name = get_object_or_404(User, username=otchet.reelt9)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)
            if otchet.reelt10:
                name = get_object_or_404(User, username=otchet.reelt10)
                s1 = s1 + '; ' + str(name.first_name) + ' ' + str(name.last_name)

            if otchet.reelt1:
                u_id = User.objects.get(username=otchet.reelt1).groups.get().name
                if u_id:
                    otchet.otd_reelt1 = str(u_id)
            if otchet.reelt2:
                u_id2 = User.objects.get(username=otchet.reelt2).groups.get().name
                if u_id2:
                    otchet.otd_reelt2 = str(u_id2)
            if otchet.reelt3:
                u_id3 = User.objects.get(username=otchet.reelt3).groups.get().name
                if u_id3:
                    otchet.otd_reelt3 = str(u_id3)
            if otchet.reelt4:
                u_id4 = User.objects.get(username=otchet.reelt4).groups.get().name
                if u_id4:
                    otchet.otd_reelt4 = str(u_id4)
            if otchet.reelt5:
                u_id5 = User.objects.get(username=otchet.reelt5).groups.get().name
                if u_id5:
                    otchet.otd_reelt5 = str(u_id5)
            if otchet.reelt6:
                u_id6 = User.objects.get(username=otchet.reelt6).groups.get().name
                if u_id6:
                    otchet.otd_reelt6 = str(u_id6)
            if otchet.reelt7:
                u_id7 = User.objects.get(username=otchet.reelt7).groups.get().name
                if u_id7:
                    otchet.otd_reelt7 = str(u_id7)
            if otchet.reelt8:
                u_id8 = User.objects.get(username=otchet.reelt8).groups.get().name
                if u_id8:
                    otchet.otd_reelt8 = str(u_id8)
            if otchet.reelt9:
                u_id9 = User.objects.get(username=otchet.reelt9).groups.get().name
                if u_id9:
                    otchet.otd_reelt9 = str(u_id9)
            if otchet.reelt10:
                u_id10 = User.objects.get(username=otchet.reelt10).groups.get().name
                if u_id10:
                    otchet.otd_reelt10 = str(u_id10)

            otchet.all_rielts = s1
            #if otchet.vneseno_komisii:
            #    otchet.vneseno_komisii_date = datetime.now()
            #if otchet.vneseno_komisii2:
            #    otchet.vneseno_komisii_date2 = datetime.now()
            #if otchet.vneseno_komisii3:
            #    otchet.vneseno_komisii_date3 = datetime.now()
            #if otchet.vneseno_komisii3:
            #    otchet.vneseno_komisii_date3 = datetime.now()
            #if otchet.vneseno_komisii3:
            #    otchet.vneseno_komisii_date3 = datetime.now()
            otchet.save()
            otchet=form.save(commit=False)
            otchet.save()
            return redirect('crm:otch_all_reelt')
    else:
        n1 = 'Отчет по сделке'
        n2 = 'редакция'
        form = otchet_all_form1(instance=otchet)
        save = 'Сохранить отчет по сделке'
        id = otchet.pk
        if otchet.sdelka_zakrita=='Рассрочка':
            rasr_pr = 'rasr'
        else:
            rasr_pr = 'No_rasr'
    return render(request, 'any/newotchet.html',{'tpotchformall':form,'tn11': n1, 'tn22': n2,  'tsave':save, 'tgroup':group, 'tid':id, 'tRasrPr':rasr_pr})

def sdelka_zakritie_view(request, idd):
    sdelka = get_object_or_404(otchet_nov, pk = idd)
    sdelka.sdelka_zakrita='Да'
    sdelka.date_zakr = timezone.localdate()
    sdelka.save()
    return redirect('crm:otch_all_reelt')

def sdelka_sriv_view(request, idd):
    sdelka = get_object_or_404(otchet_nov, pk = idd)
    sdelka.sdelka_zakrita='Срыв'
    sdelka.date_zakr = timezone.datetime.now()
    sdelka.save()
    return redirect('crm:otch_all_reelt')

def sdelka_rasroch_view(request, idd):
    sdelka = get_object_or_404(otchet_nov, pk = idd)
    sdelka.sdelka_zakrita='Рассрочка'
    sdelka.save()
    return redirect('crm:otch_all_reelt')

def sdelka_delete_view(request, idd):
    sdelka = get_object_or_404(otchet_nov, pk = idd)
    sdelka.delete()
    #sdelka.save()
    return redirect('crm:otch_all_reelt')



@login_required
def newvigrView(request):
    n1 = 'Новый обьект на выгрузку'
    n2 = 'Основные данные'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    if request.POST:
        form = vigruzkaForm(request.POST)
        if form.is_valid():
            etag = form.cleaned_data['etag']
            etagnost = form.cleaned_data['etagnost']
            if int(etag) > int(etagnost):
                n3 = 'Ошибка! Этажность меньше Этажа!'
                return render(request, 'any/vigrform.html', {'tpform': form, 'tn1': n1, 'tn2': n2, 'tn3':n3})
            else:
                feed = form.save(commit = False)
                feed.author = request.user
                feed.save()
            return redirect('crm:newvigrgal', idd = feed.pk)
    else:
        form = vigruzkaForm()

    return render(request,'any/vigrform.html',{'tpform':form, 'tn1':n1, 'tn2':n2, 'tn3':n3,'tcrm_obj_week_count':crm_obj_week_count,})

@login_required
def newvigrNovostroikaView(request):
    n1 = 'Новый обьект на выгрузку'
    n2 = 'Основные данные'
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n3 = zayavka.objects.filter(status='Свободен').count()
    if request.POST:
        form = vigruzkaNovostroikaForm(request.POST)
        if form.is_valid():
            etag = form.cleaned_data['etag']
            etagnost = form.cleaned_data['etagnost']
            if int(etag) > int(etagnost):
                n31 = 'Ошибка! Этажность меньше Этажа!'
                return render(request, 'any/vigrform.html', {'tpform': form, 'tn1': n1, 'tn2': n2, 'tn31':n31,'tcrm_obj_week_count':crm_obj_week_count,})
            else:
                feed = form.save(commit = False)
                feed.category ='newBuildingFlatSale'
                feed.author = request.user
                feed.save()
            return redirect('crm:newvigrgal', idd = feed.pk)
    else:
        form = vigruzkaNovostroikaForm()

    return render(request,'any/vigrform.html',{'tpform':form, 'tn1':n1, 'tn2':n2, 'tn3':n3,'tcrm_obj_week_count':crm_obj_week_count,})


@login_required
def newVigGalView(request, idd):
    n1 = 'Редактировать фото'
    n2 = 'Фото'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    if request.POST:
        form = vigruzkaGaleryForm(request.POST, request.FILES)
        if form.is_valid():
            feed_gallery=form.save(commit=False)
            feed_gallery.id_gal_id = idd
            feed_gallery.save()
            return redirect('crm:newvigrgal', idd=feed_gallery.id_gal_id)
    else:
        form = vigruzkaGaleryForm()
        sp = get_object_or_404(feed, pk=idd)
    return render(request,'any/vigGalForm.html',{'tpform':form, 'tn1':n1, 'tn2':n2, 'tn3':n3,'post':sp,'tcrm_obj_week_count':crm_obj_week_count,})




@login_required
def cianindexview(request):
    n1 = 'Выгрузки'
    n2 = 'Опубликованно ЦИАН'
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n3 = ''
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    sp=feed.objects.filter(author=request.user,pub='Да').order_by('-date_sozd')
    #up_sp = feed.objects.filter(author=request.user, pub='Нет').order_by('-date_sozd')
    return render(request,'any/indexcian.html',{'tsp':sp, 'tn1':n1, 'tn2':n2, 'tn3':n3,'t_my_ya_obj':my_ya_obj,'tcrm_obj_week_count':crm_obj_week_count,})

@login_required
def cianindexUPview(request):
    n1 = 'Выгрузки'
    n2 = 'Не опубликованно'
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    #sp=feed.objects.filter(author=request.user,pub='Да').order_by('-date_sozd')
    sp = feed.objects.filter(author=request.user, pub='Нет').order_by('-date_sozd')
    return render(request,'any/indexcian.html',{'tsp':sp, 'tn1':n1, 'tn2':n, 'tn3':n3,'t_my_ya_obj':my_ya_obj,'tcrm_obj_week_count':crm_obj_week_count,})

@login_required
def cianedit(request,idd):
    n1 = 'Выгрузки'
    n2 = 'Редактировать обьект'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    subj = get_object_or_404(feed, pk=idd)
    if request.POST:
        form=vigruzkaForm(request.POST,instance=subj)
        if form.is_valid():
            form.save()
            return redirect('crm:cianindex')
    else:
        form = vigruzkaForm(instance=subj)
    return render(request,'any/vigrform.html', {'tpform':form, 'tn1':n1, 'tn2':n2, 'tn3':n3,'t_my_ya_obj':my_ya_obj,'tcrm_obj_week_count':crm_obj_week_count,})

@login_required
def ciandelview(request, idd, sidd):
    n1 = 'Редактировать фото'
    n2 = 'Фото'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    spsubj = feed_gallery.objects.get(pk=sidd)
    spsubj.delete()
    sp = get_object_or_404(feed, pk=idd)
    form = vigruzkaGaleryForm()
    return redirect('crm:newvigrgal', idd=sp.pk)

@login_required
def cianDelviewSubjct(request, idd):
    spsubj = feed.objects.get(pk=idd)
    spsubj.delete()
    return redirect('crm:cianindex')

@login_required
def domclick_Index_view(request):
    pub = flat_obj.objects.filter(domclick_pub='Да')
    unpub = flat_obj.objects.filter(domclick_pub='Нет', domclick='Да')
    return render(request,'crm/flat/domclick_index.html', {'tppub':pub, 'tpupub':unpub})


########################################################
################# Zayavka
#######################################################

@login_required
def New_Zayavka_View(request):
    group = request.user.groups.get().name
    n1 = 'Новая'
    n2 = 'заявка'
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    if request.POST:
        if group == 'Юристы':
            form = Urist_new_zayavka_Form(request.POST)
            if form.is_valid():
                zayavka = form.save(commit = False)
                zayavka.author = group
                zayavka.date_zakr = timezone.datetime.now()
                zayavka.reelt_v_rabote =request.user
                zayavka.kanal = 'Домклик'
                zayavka.save()
                return redirect('crm:indexZayavka')
        else:
            form = all_zayav_form(request.POST)
            if form.is_valid():
                zayavka = form.save(commit=False)
                zayavka.author = request.user
                zayavka.reelt_v_rabote = request.user
                zayavka.date_sozd = timezone.datetime.now()
                zayavka.date_zakr = timezone.datetime.now()
                zayavka.save()
                return redirect('crm:indexZayavka')
    else:
        if group == 'Юристы':
            form = Urist_new_zayavka_Form()
        else:
            form = all_zayav_form()
    return render(request,'crm/zayavka/newUristZayav.html',{'tpform':form, 'tn1':n1, 'tn2':n2,'t_my_ya_obj':my_ya_obj
                                                            ,'tcrm_obj_week_count': crm_obj_week_count,})
@login_required
def New_Nov_Zayavka_View(request):
    if request.POST:
        form = nov_new_zayv_form(request.POST)
        if form.is_valid():
            zayavka = form.save(commit=False)
            zayavka.author =request.user
            zayavka.reelt_v_rabote = request.user
            zayavka.date_sozd = timezone.datetime.now()
            zayavka.date_zakr = timezone.datetime.now()
            zayavka.kanal = 'Заявка с сайта новостройка'
            zayavka.save()
            return redirect('crm:indexZayavka')
    else:
        form =  nov_new_zayv_form()
    return render(request,'crm/zayavka/newUristZayav.html',{'tpform':form})

@login_required
def lich_rielt_Zayavka_View(request):
    if request.POST:
        form = reelt_lich_new_zayv_form(request.POST)
        if form.is_valid():
            zayavka = form.save(commit=False)
            zayavka.author =request.user
            #zayavka.reelt_v_rabote = request.user
            zayavka.date_sozd = timezone.datetime.now()
            zayavka.date_zakr = timezone.datetime.now()
            zayavka.kanal = 'Заявка с сайта новостройка'
            zayavka.status = 'Взят в работу'
            zayavka.save()
            return redirect('crm:indexZayavka')
    else:
        form =  reelt_lich_new_zayv_form()
    return render(request,'crm/zayavka/newUristZayav.html',{'tpform':form})

@login_required
def zaiyavka_Index_view(request):
    n1 = 'Поступившие'
    n2 = 'в компанию заявки'
    d11 = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday())
    poned = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday()) - timedelta(days=7)
    voskr = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday()) - timedelta(
        days=7) + timedelta(days=6)
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    date = datetime.now() - timedelta(days=10)
    open_zayavki = zayavka.objects.filter(status='Свободен').order_by('-date_sozd')
    group = request.user.groups.get().name
    if group == 'Администрация' or group =='Администрация Адлер' or group =='Офис-менеджер' or group == 'Юристы':
        n4 = zayavka.objects.filter(status='Взят в работу',).count()
        vzyati_zayavki = zayavka.objects.filter(status='Взят в работу').order_by('-date_sozd')

        n5 = zayavka.objects.filter(status='Срыв',).count()
        sriv_zayavki = zayavka.objects.filter(status='Срыв').order_by('-date_sozd')

        n6 = zayavka.objects.filter(status='Сделка',).count()
        sdelka_zayavki = zayavka.objects.filter(status='Сделка').order_by('-date_sozd').order_by('-date_sozd')
        butn_pr='Yes'
    else:
        n4 = zayavka.objects.filter(status='Взят в работу', reelt_v_rabote=request.user).count()
        vzyati_zayavki = zayavka.objects.filter(status='Взят в работу', reelt_v_rabote=request.user).order_by(
            '-date_sozd')

        n5 = zayavka.objects.filter(status='Срыв', reelt_v_rabote=request.user).count()
        sriv_zayavki = zayavka.objects.filter(status='Срыв', reelt_v_rabote=request.user).order_by(
            '-date_sozd')

        n6 = zayavka.objects.filter(status='Сделка', reelt_v_rabote=request.user).count()
        sdelka_zayavki = zayavka.objects.filter(status='Сделка', reelt_v_rabote=request.user).order_by(
            '-date_sozd')
        if flat_obj.objects.filter(author=request.user,date_sozd__gte=poned, date_sozd__lte=voskr).count()>=5:
            butn_pr = 'Yes'
        else:
            butn_pr ='no'
    return render(request,'crm/zayavka/index.html',{'topen_zayavki':open_zayavki, 'tvzyati_zayavki':vzyati_zayavki,
                                                    'tsriv_zayavki': sriv_zayavki,'tsdelka_zayavki': sdelka_zayavki,
                                                    't_my_ya_obj':my_ya_obj,'tgroup':group,'tbutn_pr':butn_pr,
                                                    'tn1':n1, 'tn2':n2, 'tn3':n3,'tn4':n4,'tn5':n5,'tn6':n6,
                                                    'tcrm_obj_week_count':crm_obj_week_count,} )

@login_required
def zayavka_vzyata_view(request, idd):
    post = get_object_or_404(zayavka, pk = idd)
    post.status = 'Взят в работу'
    post.reelt_v_rabote = request.user
    post.save()
    return redirect('crm:indexZayavka')


@login_required
def zayavka_sdelka_view(request, idd):
    post = get_object_or_404(zayavka, pk = idd)
    post.status = 'Сделка'
    post.date_zakr = timezone.datetime.now()
    post.reelt_v_rabote = request.user
    post.save()
    return redirect('crm:indexZayavka')

@login_required
def zayavka_sriv_view(request, idd):
    n1 = 'Поступившие'
    n2 = 'в компанию заявки'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    post = get_object_or_404(zayavka, pk = idd)
    n3 = zayavka.objects.filter(status='Свободен').count()
    n4 = zayavka.objects.filter(status='Взят в работу', reelt_v_rabote=request.user).count()
    open_zayavki = zayavka.objects.filter(status='Свободен').order_by('-date_sozd').order_by('-date_sozd')
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    vzyati_zayavki = zayavka.objects.filter(status='Взят в работу', reelt_v_rabote=request.user).order_by(
        '-date_sozd').order_by('-date_sozd')

    if request.POST:
        form = sriv_zayavka_form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.status = 'Срыв'
            post.date_zakr = timezone.datetime.now()
            post.save()
            return redirect('crm:indexZayavka')
    else:

        form = sriv_zayavka_form(instance=post)
    return render(request,'crm/zayavka/newUristZayav.html',{'tpform':form, 'tn1':n1, 'tn2':n2,'tn3':n3,'tn4':n4,
                                                            't_my_ya_obj': my_ya_obj,
                                                            'topen_zayavki':open_zayavki, 'tvzyati_zayavki':vzyati_zayavki
                                                            , 'tcrm_obj_week_count': crm_obj_week_count,} )


#############################################
### Statistica po kol-vu objects tek nedelya
############################################


@login_required
def stat_count_crm_obj(request):
    d1 = timezone.datetime.now().date()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n1 = 'Статистика'
    n2 = 'CRM текущая неделя'
    if request.user.userprofile1.nach_otd =='Да' or request.user.groups.get().name=='Администрация' or request.user.groups.get().name=='Администрация Адлер':
        nach_otd='Yes'
    else:
        nach_otd='No'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    stat_obj_crm.objects.all().delete()
    user = User.objects.all()
    for i in user:
        if i.is_active:
            date = datetime.now() - timedelta(days=10)
            #cian_count = feed.objects.filter(author_id=i.id, pub='Да', date_sozd__gte=date).order_by('-date_sozd').count()
            cian_count = flat_obj.objects.filter(author_id=i.id, status_gilya='Нежилое помещение', date_sozd__gte=d11, date_sozd__lt=d1 ).order_by(
                '-date_sozd').count()
            countss =flat_obj.objects.filter(author_id=i.id).count()
            countss_kadastr = flat_obj.objects.filter(author_id=i.id).exclude(kadastr='').count()
            countss_w = flat_obj.objects.filter(author_id=i.id, date_sozd__gte=d11).count()
            s = stat_obj_crm(auth_nic  = i.username, auth_ful_name = i.first_name +' '+i.last_name, auth_group = i.groups.get().name,
                             crm_calc_week= countss_w ,crm_calc_kadastr=countss_kadastr ,crm_calc = countss, cian_calc=cian_count)
            s.save()


    otdel1 = stat_obj_crm.objects.filter(auth_group='1 Отдел').order_by('-crm_calc')
    otdel2 = stat_obj_crm.objects.filter(auth_group='2 Отдел').order_by('-crm_calc')
    otdel3 = stat_obj_crm.objects.filter(auth_group='3 Отдел').order_by('-crm_calc')
    otdel4 = stat_obj_crm.objects.filter(auth_group='4 Отдел').order_by('-crm_calc')
    AdlOtdel = stat_obj_crm.objects.filter(auth_group__contains='Адлер').order_by(('-crm_calc'))

    otdel1_cn1 = stat_obj_crm.objects.filter(auth_group='1 Отдел').aggregate(Sum('crm_calc'))
    otdel1_cn = str(otdel1_cn1.get('crm_calc__sum'))
    otdel2_cn1 = stat_obj_crm.objects.filter(auth_group='2 Отдел').aggregate(Sum('crm_calc'))
    otdel2_cn = str(otdel2_cn1.get('crm_calc__sum'))
    otdel3_cn1 = stat_obj_crm.objects.filter(auth_group='3 Отдел').aggregate(Sum('crm_calc'))
    otdel3_cn = str(otdel3_cn1.get('crm_calc__sum'))
    otdel4_cn1 = stat_obj_crm.objects.filter(auth_group='4 Отдел').aggregate(Sum('crm_calc'))
    otdel4_cn = str(otdel4_cn1.get('crm_calc__sum'))
    AdlOtdel_cn1 = stat_obj_crm.objects.filter(auth_group='Офис в Адлере').aggregate(Sum('crm_calc'))
    AdlOtdel_cn = str(AdlOtdel_cn1.get('crm_calc__sum'))

    vestum = flat_obj.objects.filter(status_gilya='Нежилое помещение').exclude(kadastr='').count()
    egr = flat_obj.objects.all().exclude(kadastr='').count()
    all1 = stat_obj_crm.objects.all().aggregate(Sum('crm_calc'))
    all = str(all1.get('crm_calc__sum'))
    return render(request,'crm/stat/crm_obj_index.html',
                    {'tOtd1':otdel1,'tOtd2':otdel2,'tOtd3':otdel3,'tOtd4':otdel4,
                   'tOtd1_cn':otdel1_cn,'tOtd2_cn':otdel2_cn,'tOtd3_cn':otdel3_cn,
                   'tAdlOtdel':AdlOtdel,
                   'tOtd4_cn': otdel4_cn, 'tOtdAdl_cn': AdlOtdel_cn,'tall':all,
                     't_my_ya_obj': my_ya_obj,'tNach_otd':nach_otd, 'tegr':egr,'tvs':vestum,
                     'tn1': n1, 'tn2': n2, 'tn3': n3, 'td1':d1, 'td11':d11,'tcrm_obj_week_count':crm_obj_week_count,
                     })


#############################################
### Statistica po kol-vu objects proshlaya nedelya
############################################


@login_required
def stat_count_crm_obj_past(request):
    #d1 = timezone.datetime.now().date()
    d1 = timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    d11 = timezone.datetime.now().date()-timedelta(days=7)
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    n1 = 'Статистика'
    n2 = 'CRM прошлая неделя'
    if request.user.userprofile1.nach_otd =='Да' or request.user.groups.get().name=='Администрация' or request.user.groups.get().name=='Администрация Адлер':
        nach_otd='Yes'
    else:
        nach_otd='No'
    n3 = zayavka.objects.filter(status='Свободен').count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()
    stat_obj_crm.objects.all().delete()
    user = User.objects.all()
    for i in user:
        if i.is_active:
            date = datetime.now() - timedelta(days=10)
            #cian_count = feed.objects.filter(author_id=i.id, pub='Да', date_sozd__gte=date).order_by('-date_sozd').count()
            cian_count = flat_obj.objects.filter(author_id=i.id, status_gilya='Нежилое помещение', date_sozd__gte=d11, date_sozd__lt=d1 ).order_by(
                '-date_sozd').count()
            countss =flat_obj.objects.filter(author_id=i.id).count()
            countss_kadastr = flat_obj.objects.filter(author_id=i.id).exclude(kadastr='').count()
            countss_w = flat_obj.objects.filter(author_id=i.id, date_sozd__gte=d11, date_sozd__lt=d1).count()
            s = stat_obj_crm(auth_nic  = i.username, auth_ful_name = i.first_name +' '+i.last_name, auth_group = i.groups.get().name,
                             crm_calc_week= countss_w ,crm_calc_kadastr=countss_kadastr ,crm_calc = countss, cian_calc=cian_count)
            s.save()


    otdel1 = stat_obj_crm.objects.filter(auth_group='1 Отдел').order_by('-crm_calc')
    otdel2 = stat_obj_crm.objects.filter(auth_group='2 Отдел').order_by('-crm_calc')
    otdel3 = stat_obj_crm.objects.filter(auth_group='3 Отдел').order_by('-crm_calc')
    otdel4 = stat_obj_crm.objects.filter(auth_group='4 Отдел').order_by('-crm_calc')
    AdlOtdel = stat_obj_crm.objects.filter(auth_group__contains='Адлер').order_by(('-crm_calc'))


    otdel1_cn1 = stat_obj_crm.objects.filter(auth_group='1 Отдел').aggregate(Sum('crm_calc'))
    otdel1_cn = str(otdel1_cn1.get('crm_calc__sum'))
    otdel2_cn1 = stat_obj_crm.objects.filter(auth_group='2 Отдел').aggregate(Sum('crm_calc'))
    otdel2_cn = str(otdel2_cn1.get('crm_calc__sum'))
    otdel3_cn1 = stat_obj_crm.objects.filter(auth_group='3 Отдел').aggregate(Sum('crm_calc'))
    otdel3_cn = str(otdel3_cn1.get('crm_calc__sum'))
    otdel4_cn1 = stat_obj_crm.objects.filter(auth_group='4 Отдел').aggregate(Sum('crm_calc'))
    otdel4_cn = str(otdel4_cn1.get('crm_calc__sum'))
    AdlOtdel_cn1 = stat_obj_crm.objects.filter(auth_group='Офис в Адлере').aggregate(Sum('crm_calc'))
    AdlOtdel_cn = str(AdlOtdel_cn1.get('crm_calc__sum'))

    vestum = flat_obj.objects.filter(vestum_pub='Да').count()
    egr = flat_obj.objects.all().exclude(kadastr='').count()
    all1 = stat_obj_crm.objects.all().aggregate(Sum('crm_calc'))
    all = str(all1.get('crm_calc__sum'))
    return render(request,'crm/stat/crm_obj_index.html',
                    {'tOtd1':otdel1,'tOtd2':otdel2,'tOtd3':otdel3,'tOtd4':otdel4,
                   'tOtd1_cn':otdel1_cn,'tOtd2_cn':otdel2_cn,'tOtd3_cn':otdel3_cn,
                   'tAdlOtdel':AdlOtdel,
                   'tOtd4_cn': otdel4_cn, 'tOtdAdl_cn': AdlOtdel_cn,'tall':all,
                     't_my_ya_obj': my_ya_obj,'tNach_otd':nach_otd, 'tegr':egr,'tvs':vestum,
                     'tn1': n1, 'tn2': n2, 'tn3': n3, 'td1':d1, 'td11':d11,'tcrm_obj_week_count':crm_obj_week_count,
                     })

#############################################
### reiting SDELKI
### main & month
############################################

@login_required
def reyting_po_sdelkam_view(request):
    n1 = 'Рейтинг компании'
    date_end = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day)
    #locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    n2 =  'за текущий месяц'
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()

    if request.POST:
        form =  search_by_moth_form(request.POST)
        if form.is_valid():
            mothf = form.cleaned_data['month']
            mothf1 = form.cleaned_data['month']
            yearf = form.cleaned_data['year']
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'

            date_start = yearf+'-'+mothf+'-'+'01'
            date_end =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year, int(mothf))[1])
            n2 = 'c ' + date_start + ' по ' + date_end
            SearchMonthForm = search_by_moth_form(initial={'year': yearf, 'month' : mothf1})
    else:
        date_end = timezone.datetime.now()
        date_start = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day-1)
        SearchMonthForm = search_by_moth_form()

    #SearchMonthForm = search_by_moth_form()
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name=='Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name =user.last_name + ' '+user.first_name
#################################################
##### Kol Sdelok                            ###
#################################################
                        sdelki_count = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Да',
                                                                 date_zakr__lte=date_end, date_zakr__gte=date_start).count()
#################################################
##### Kol _subj_Cian                            ###
#################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                         date_sozd__lte=date_end, date_sozd__gte=date_start).count()
#################################################
##### Kol Subj CRM                            ###
#################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                                 #date_sozd__lte=date_end, date_sozd__gte=date_start).count()


#################################################
##### Summa Sdelok                            ###
#################################################
                        sdelki_sum = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Да',
                                                               date_zakr__lte= date_end, date_zakr__gte=date_start)

                        r_sum=0
                        rasr_sum1 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date__lte= date_end,
                                                             vneseno_komisii_date__gte=date_start)
                        if rasr_sum1:
                            rasr_sum1 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date__lte=date_end,
                                vneseno_komisii_date__gte=date_start).aggregate(Sum("vneseno_komisii"))
                            if rasr_sum1.get('vneseno_komisii__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii__sum') * 50 / 100))
                            else:
                                r_sum = r_sum
                        else:
                            r_sum=0

                        rasr_sum2 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date2__lte= date_end,
                                                             vneseno_komisii_date2__gte=date_start)
                        if rasr_sum2:
                            rasr_sum2 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date2__lte=date_end,
                                vneseno_komisii_date2__gte=date_start
                                ).aggregate(Sum("vneseno_komisii2"))
                            if rasr_sum2.get('vneseno_komisii2__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum2.get('vneseno_komisii2__sum') * 50 / 100))
                            else:
                                r_sum = r_sum


                        rasr_sum3 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date3__lte= date_end,
                                                             vneseno_komisii_date3__gte=date_start)
                        if rasr_sum3:
                            rasr_sum3 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date3__lte=date_end,
                                vneseno_komisii_date3__gte=date_start).aggregate(Sum("vneseno_komisii3"))
                            if rasr_sum3.get('vneseno_komisii3__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii3__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum4 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date4__lte= date_end,
                                                            vneseno_komisii_date4__gte=date_start)
                        if rasr_sum4:
                            rasr_sum4 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date4__lte=date_end,
                                vneseno_komisii_date4__gte=date_start).aggregate(Sum("vneseno_komisii4"))
                            if rasr_sum4.get('vneseno_komisii4__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii4__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum5 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date5__lte= date_end,
                                                             vneseno_komisii_date5__gte=date_start)
                        if rasr_sum5:
                            rasr_sum5 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date5__lte=date_end,
                                vneseno_komisii_date5__gte=date_start).aggregate(Sum("vneseno_komisii5"))
                            if rasr_sum5.get('vneseno_komisii5__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii5__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        sum=0
                        sum = sum + int(r_sum)
                        for i in sdelki_sum:
                            if i.reelt1 ==  user.username:
                                sum = sum+((i.komisia/2)*i.rielt_proc1/100)*2
                            if i.reelt2 ==  user.username:
                                sum = sum+((i.komisia/2)*i.rielt_proc2/100)*2
                            if i.reelt3 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc3/100)*2
                            if i.reelt4 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc4/100)*2
                            if i.reelt5 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc5/100)*2
                            if i.reelt6 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc6/100)*2
                            if i.reelt7 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc7/100)*2
                            if i.reelt8 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc8/100)*2
                            if i.reelt9 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc9/100)*2
                            if i.reelt10 ==  user.username:
                                sum =  sum+((i.komisia/2)*i.rielt_proc10/100)*2
                            sum=sum+int(r_sum)
                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name, sdelok_calc=sdelki_count,
                                               sdelok_sum= sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
 ##########################
 # all For Sochi
 #########################
    zero_bal = reyting_po_sdelkam.objects.filter( sdelok_sum =0,).exclude(auth_group__in=['Офис в Адлере','Администрация Адлер','seo'])
    udl_bal  = reyting_po_sdelkam.objects.filter( sdelok_sum__lte = 80000, sdelok_sum__gt=1).order_by('-sdelok_sum').exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000, sdelok_sum__gt=80000).order_by('-sdelok_sum').exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter( sdelok_sum__gt=120000).order_by('-sdelok_sum').exclude(auth_group__in=['Офис в Адлере','Администрация Адлер'])
 ###########################
 # all For Adler
 ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter( sdelok_sum =0, auth_group__in=['Офис в Адлере','Администрация Адлер'] )
    Audl_bal  = reyting_po_sdelkam.objects.filter( sdelok_sum__lte = 80000, sdelok_sum__gt=1,auth_group__in=['Офис в Адлере','Администрация Адлер'] ).order_by('-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000, sdelok_sum__gt=80000,auth_group__in=['Офис в Адлере','Администрация Адлер'] ).order_by('-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter( sdelok_sum__gt=120000, auth_group__in=['Офис в Адлере','Администрация Адлер'] ).order_by('-sdelok_sum')
##########################
# reiting in otdel for nach otdel
#########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000, sdelok_sum__gt=80000, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000, auth_group=gr).order_by('-sdelok_sum')
##########################
# reiting in otdel for Golovin
#########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел'or i.name == '2 Отдел'or i.name == '3 Отдел'or i.name == '4 Отдел':
            if i.name=='Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum)+int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                if str(sum) == 'None':
                    sum = 0
                s = reyt_sdelka_otd(otd = i.name, kommisia = sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    return render(request,'crm/stat/sdelkareyting.html',{'zero':zero_bal, 'udl':udl_bal, 'good':good_bal,'great':great_bal,
                'Azero': Azero_bal, 'Audl': Audl_bal, 'Agood': Agood_bal, 'Agreat': Agreat_bal,
                'tn1':n1, 'tn2':n2,'tn3':n3,'tcrm_obj_week_count':crm_obj_week_count,'tnach':nach_pr,
                 't_my_ya_obj': my_ya_obj, 'MForm': SearchMonthForm, 't11':Alsum, 'tdate':date_start,
                 'Nzero': Nzero_bal, 'Nudl': Nudl_bal, 'Ngood': Ngood_bal, 'Ngreat': Ngreat_bal,'todtd':otd_reit, 't':date_end })

#@login_required
#def reyting_po_sdelkam_mSearch_view(request):
#    #moth =
#    ds = timezone.datetime.now()-timedelta(days=timezone.datetime.now().day)-timedelta(days=1)
#    de = calendar.monthrange(2002,2)[1]
#    return render(request,'crm/stat/temp.html',{'tds':ds, 'tde': de})



#############################################
### Statistica po kol-vu objects & SDELKI
### 1 kvartal
############################################
@login_required
def reyting_po_sdelkam_mSearch_view(request):
    n1 = 'Рейтинг компании'
    date_end = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day)
    n2 ='C '+str(timezone.datetime.now().year)+'-01-01'+ ' по '+ str(timezone.datetime.now().year)+'-03-'+str(calendar.monthrange(timezone.datetime.now().year,1)[1])
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()

    if request.POST:
        form =  search_by_moth_form(request.POST)
        if form.is_valid():
            mothf = form.cleaned_data['month']
            mothf1 = form.cleaned_data['month']
            yearf = form.cleaned_data['year']
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'

            date_start = yearf+'-'+mothf+'-'+'01'
            date_end =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year,int(mothf))[1])
            n2 = 'c ' + date_start + 'по ' + date_end
            prizn = 1
            SearchMonthForm = search_by_moth_form(initial={'year': yearf, 'month': mothf1})
    else:
        date_start = str(timezone.datetime.now().year) + '-01-01'
        date_end = str(timezone.datetime.now().year) + '-03-' + str(
            calendar.monthrange(timezone.datetime.now().year, 3)[1])
        n2 = 'c ' + date_start + ' по ' + date_end + '(1 Квартал)'
        prizn = 3

        SearchMonthForm = search_by_moth_form()
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name == 'Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name = user.last_name + ' '+ user.first_name
                        sdelki_count = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start).count()
                        #################################################
                        ##### Kol _subj_Cian                            ###
                        #################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                          date_sozd__lte=date_end, date_sozd__gte=date_start).count()
                        #################################################
                        ##### Kol Subj CRM                            ###
                        #################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                             #date_sozd__lte=date_end, date_sozd__gte=date_start).count()

                        #################################################
                        ##### Summa Sdelok                            ###
                        #################################################
                        sdelki_sum = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start)
                        r_sum=0
                        rasr_sum1 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date__lte= date_end,
                                                             vneseno_komisii_date__gte=date_start)
                        if rasr_sum1:
                            rasr_sum1 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date__lte=date_end,
                                vneseno_komisii_date__gte=date_start).aggregate(Sum("vneseno_komisii"))
                            if rasr_sum1.get('vneseno_komisii__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii__sum') * 50 / 100))
                            else:
                                r_sum = r_sum
                        else:
                            r_sum=0

                        rasr_sum2 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date2__lte= date_end,
                                                             vneseno_komisii_date2__gte=date_start)
                        if rasr_sum2:
                            rasr_sum2 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date2__lte=date_end,
                                vneseno_komisii_date2__gte=date_start
                                ).aggregate(Sum("vneseno_komisii2"))
                            if rasr_sum2.get('vneseno_komisii2__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum2.get('vneseno_komisii2__sum') * 50 / 100))
                            else:
                                r_sum = r_sum


                        rasr_sum3 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date3__lte= date_end,
                                                             vneseno_komisii_date3__gte=date_start)
                        if rasr_sum3:
                            rasr_sum3 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date3__lte=date_end,
                                vneseno_komisii_date3__gte=date_start).aggregate(Sum("vneseno_komisii3"))
                            if rasr_sum3.get('vneseno_komisii3__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii3__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum4 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date4__lte= date_end,
                                                            vneseno_komisii_date4__gte=date_start)
                        if rasr_sum4:
                            rasr_sum4 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date4__lte=date_end,
                                vneseno_komisii_date4__gte=date_start).aggregate(Sum("vneseno_komisii4"))
                            if rasr_sum4.get('vneseno_komisii4__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii4__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum5 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date5__lte= date_end,
                                                             vneseno_komisii_date5__gte=date_start)
                        if rasr_sum5:
                            rasr_sum5 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date5__lte=date_end,
                                vneseno_komisii_date5__gte=date_start).aggregate(Sum("vneseno_komisii5"))
                            if rasr_sum5.get('vneseno_komisii5__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii5__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        sum=0
                        sum = sum + int(r_sum)
                        for i in sdelki_sum:
                            if i.reelt1 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc1 / 100) * 2
                            if i.reelt2 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc2 / 100) * 2
                            if i.reelt3 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc3 / 100) * 2
                            if i.reelt4 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc4 / 100) * 2
                            if i.reelt5 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc5 / 100) * 2
                            if i.reelt6 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc6 / 100) * 2
                            if i.reelt7 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc7 / 100) * 2
                            if i.reelt8 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc8 / 100) * 2
                            if i.reelt9 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc9 / 100) * 2
                            if i.reelt10 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc10 / 100) * 2

                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name,
                                               sdelok_calc=sdelki_count,
                                               sdelok_sum=sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
    ##########################
    # all For Sochi
    #########################
    zero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, ).exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер','seo'])
    udl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn).order_by('-sdelok_sum').exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    ###########################
    # all For Adler
    ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    Audl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1,
                                                 auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn,
                                                  auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn,
                                                   auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    ##########################
    # reiting in otdel for nach otdel
    #########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn, auth_group=gr).order_by('-sdelok_sum')
    ##########################
    # reiting in otdel for Golovin
    #########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел' or i.name == '2 Отдел' or i.name == '3 Отдел' or i.name == '4 Отдел':
            if i.name == 'Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum) + int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                s = reyt_sdelka_otd(otd=i.name, kommisia=sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    return render(request, 'crm/stat/sdelkareyting.html',
                  {'zero': zero_bal, 'udl': udl_bal, 'good': good_bal, 'great': great_bal,
                   'Azero': Azero_bal, 'Audl': Audl_bal, 'Agood': Agood_bal, 'Agreat': Agreat_bal,
                   'tn1': n1, 'tn2': n2, 'tn3': n3, 'tcrm_obj_week_count': crm_obj_week_count, 'tnach': nach_pr,
                   't_my_ya_obj': my_ya_obj, 'MForm': SearchMonthForm, 't11': Alsum,
                   'Nzero': Nzero_bal, 'Nudl': Nudl_bal, 'Ngood': Ngood_bal, 'Ngreat': Ngreat_bal, 'todtd': otd_reit})

#############################################
### Statistica po kol-vu objects & SDELKI
### 2 kvartal
############################################
@login_required
def reyting_po_sdelkam_2Kvartal_view(request):
    n1 = 'Рейтинг компании'
    date_end = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day)
    n2 ='C '+str(timezone.datetime.now().year)+'-01-01'+ ' по '+ str(timezone.datetime.now().year)+'-03-'+str(calendar.monthrange(timezone.datetime.now().year,1)[1])
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()

    if request.POST:
        form =  search_by_moth_form(request.POST)
        if form.is_valid():
            mothf = form.cleaned_data['month']
            mothf1 = form.cleaned_data['month']
            yearf = form.cleaned_data['year']
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'

            date_start = yearf+'-'+mothf+'-'+'01'
            date_end =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year, int(mothf))[1])
            n2 = 'c ' + date_start + 'по ' + date_end
            prizn = 1
            SearchMonthForm = search_by_moth_form(initial={'year': yearf, 'month': mothf1})
    else:
        date_start = str(timezone.datetime.now().year) + '-04-01'
        date_end = str(timezone.datetime.now().year) + '-06-' + str(
            calendar.monthrange(timezone.datetime.now().year, 6)[1])
        n2 = 'c ' + date_start + ' по ' + date_end + '(2 Квартал)'
        prizn = 3

        SearchMonthForm = search_by_moth_form()
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name == 'Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name = user.last_name + ' ' + user.first_name
                        sdelki_count = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start).count()
                        #################################################
                        ##### Kol _subj_Cian                            ###
                        #################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                          date_sozd__lte=date_end, date_sozd__gte=date_start).count()
                        #################################################
                        ##### Kol Subj CRM                            ###
                        #################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                             #date_sozd__lte=date_end, date_sozd__gte=date_start).count()

                        #################################################
                        ##### Summa Sdelok                            ###
                        #################################################
                        sdelki_sum = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start)
                        r_sum=0
                        rasr_sum1 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date__lte= date_end,
                                                             vneseno_komisii_date__gte=date_start)
                        if rasr_sum1:
                            rasr_sum1 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date__lte=date_end,
                                vneseno_komisii_date__gte=date_start).aggregate(Sum("vneseno_komisii"))
                            if rasr_sum1.get('vneseno_komisii__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii__sum') * 50 / 100))
                            else:
                                r_sum = r_sum
                        else:
                            r_sum=0

                        rasr_sum2 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date2__lte= date_end,
                                                             vneseno_komisii_date2__gte=date_start)
                        if rasr_sum2:
                            rasr_sum2 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date2__lte=date_end,
                                vneseno_komisii_date2__gte=date_start
                                ).aggregate(Sum("vneseno_komisii2"))
                            if rasr_sum2.get('vneseno_komisii2__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum2.get('vneseno_komisii2__sum') * 50 / 100))
                            else:
                                r_sum = r_sum


                        rasr_sum3 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date3__lte= date_end,
                                                             vneseno_komisii_date3__gte=date_start)
                        if rasr_sum3:
                            rasr_sum3 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date3__lte=date_end,
                                vneseno_komisii_date3__gte=date_start).aggregate(Sum("vneseno_komisii3"))
                            if rasr_sum3.get('vneseno_komisii3__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii3__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum4 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date4__lte= date_end,
                                                            vneseno_komisii_date4__gte=date_start)
                        if rasr_sum4:
                            rasr_sum4 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date4__lte=date_end,
                                vneseno_komisii_date4__gte=date_start).aggregate(Sum("vneseno_komisii4"))
                            if rasr_sum4.get('vneseno_komisii4__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii4__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum5 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date5__lte= date_end,
                                                             vneseno_komisii_date5__gte=date_start)
                        if rasr_sum5:
                            rasr_sum5 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date5__lte=date_end,
                                vneseno_komisii_date5__gte=date_start).aggregate(Sum("vneseno_komisii5"))
                            if rasr_sum5.get('vneseno_komisii5__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii5__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        sum=0
                        sum = sum + int(r_sum)
                        for i in sdelki_sum:
                            if i.reelt1 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc1 / 100) * 2
                            if i.reelt2 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc2 / 100) * 2
                            if i.reelt3 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc3 / 100) * 2
                            if i.reelt4 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc4 / 100) * 2
                            if i.reelt5 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc5 / 100) * 2
                            if i.reelt6 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc6 / 100) * 2
                            if i.reelt7 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc7 / 100) * 2
                            if i.reelt8 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc8 / 100) * 2
                            if i.reelt9 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc9 / 100) * 2
                            if i.reelt10 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc10 / 100) * 2

                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name,
                                               sdelok_calc=sdelki_count,
                                               sdelok_sum=sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
    ##########################
    # all For Sochi
    #########################
    zero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, ).exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер','seo'])
    udl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn).order_by('-sdelok_sum').exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    ###########################
    # all For Adler
    ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    Audl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1,
                                                 auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn,
                                                  auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn,
                                                   auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    ##########################
    # reiting in otdel for nach otdel
    #########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn, auth_group=gr).order_by('-sdelok_sum')
    ##########################
    # reiting in otdel for Golovin
    #########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел' or i.name == '2 Отдел' or i.name == '3 Отдел' or i.name == '4 Отдел':
            if i.name == 'Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum) + int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                s = reyt_sdelka_otd(otd=i.name, kommisia=sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    return render(request, 'crm/stat/sdelkareyting.html',
                  {'zero': zero_bal, 'udl': udl_bal, 'good': good_bal, 'great': great_bal,
                   'Azero': Azero_bal, 'Audl': Audl_bal, 'Agood': Agood_bal, 'Agreat': Agreat_bal,
                   'tn1': n1, 'tn2': n2, 'tn3': n3, 'tcrm_obj_week_count': crm_obj_week_count, 'tnach': nach_pr,
                   't_my_ya_obj': my_ya_obj, 'MForm': SearchMonthForm, 't11': Alsum,
                   'Nzero': Nzero_bal, 'Nudl': Nudl_bal, 'Ngood': Ngood_bal, 'Ngreat': Ngreat_bal, 'todtd': otd_reit})

#############################################
### Statistica po kol-vu objects & SDELKI
### 3 kvartal
############################################
@login_required
def reyting_po_sdelkam_3Kvartal_view(request):
    n1 = 'Рейтинг компании'
    date_end = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day)
    n2 ='C '+str(timezone.datetime.now().year)+'-01-01'+ ' по '+ str(timezone.datetime.now().year)+'-03-'+str(calendar.monthrange(timezone.datetime.now().year,1)[1])
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()

    if request.POST:
        form =  search_by_moth_form(request.POST)
        if form.is_valid():
            mothf = form.cleaned_data['month']
            mothf1 = form.cleaned_data['month']
            yearf = form.cleaned_data['year']
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'

            date_start = yearf+'-'+mothf+'-'+'01'
            date_end =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year,int(mothf))[1])
            n2 = 'c ' + date_start + 'по ' + date_end
            prizn = 1
            SearchMonthForm = search_by_moth_form(initial={'year': yearf, 'month': mothf1})
    else:
        date_start = str(timezone.datetime.now().year) + '-07-01'
        date_end = str(timezone.datetime.now().year) + '-09-' + str(
            calendar.monthrange(timezone.datetime.now().year, 9)[1])
        n2 = 'c ' + date_start + ' по ' + date_end + '(3 Квартал)'
        prizn = 3

        SearchMonthForm = search_by_moth_form()
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name == 'Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name = user.last_name + ' ' + user.first_name
                        sdelki_count = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start).count()
                        #################################################
                        ##### Kol _subj_Cian                            ###
                        #################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                          date_sozd__lte=date_end, date_sozd__gte=date_start).count()
                        #################################################
                        ##### Kol Subj CRM                            ###
                        #################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                             #date_sozd__lte=date_end, date_sozd__gte=date_start).count()

                        #################################################
                        ##### Summa Sdelok                            ###
                        #################################################
                        sdelki_sum = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start)
                        r_sum=0
                        rasr_sum1 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date__lte= date_end,
                                                             vneseno_komisii_date__gte=date_start)
                        if rasr_sum1:
                            rasr_sum1 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date__lte=date_end,
                                vneseno_komisii_date__gte=date_start).aggregate(Sum("vneseno_komisii"))
                            if rasr_sum1.get('vneseno_komisii__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii__sum') * 50 / 100))
                            else:
                                r_sum = r_sum
                        else:
                            r_sum=0

                        rasr_sum2 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date2__lte= date_end,
                                                             vneseno_komisii_date2__gte=date_start)
                        if rasr_sum2:
                            rasr_sum2 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date2__lte=date_end,
                                vneseno_komisii_date2__gte=date_start
                                ).aggregate(Sum("vneseno_komisii2"))
                            if rasr_sum2.get('vneseno_komisii2__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum2.get('vneseno_komisii2__sum') * 50 / 100))
                            else:
                                r_sum = r_sum


                        rasr_sum3 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date3__lte= date_end,
                                                             vneseno_komisii_date3__gte=date_start)
                        if rasr_sum3:
                            rasr_sum3 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date3__lte=date_end,
                                vneseno_komisii_date3__gte=date_start).aggregate(Sum("vneseno_komisii3"))
                            if rasr_sum3.get('vneseno_komisii3__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii3__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum4 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date4__lte= date_end,
                                                            vneseno_komisii_date4__gte=date_start)
                        if rasr_sum4:
                            rasr_sum4 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date4__lte=date_end,
                                vneseno_komisii_date4__gte=date_start).aggregate(Sum("vneseno_komisii4"))
                            if rasr_sum4.get('vneseno_komisii4__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii4__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum5 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date5__lte= date_end,
                                                             vneseno_komisii_date5__gte=date_start)
                        if rasr_sum5:
                            rasr_sum5 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date5__lte=date_end,
                                vneseno_komisii_date5__gte=date_start).aggregate(Sum("vneseno_komisii5"))
                            if rasr_sum5.get('vneseno_komisii5__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii5__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        sum=0
                        sum = sum + int(r_sum)
                        for i in sdelki_sum:
                            if i.reelt1 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc1 / 100) * 2
                            if i.reelt2 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc2 / 100) * 2
                            if i.reelt3 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc3 / 100) * 2
                            if i.reelt4 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc4 / 100) * 2
                            if i.reelt5 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc5 / 100) * 2
                            if i.reelt6 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc6 / 100) * 2
                            if i.reelt7 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc7 / 100) * 2
                            if i.reelt8 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc8 / 100) * 2
                            if i.reelt9 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc9 / 100) * 2
                            if i.reelt10 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc10 / 100) * 2

                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name,
                                               sdelok_calc=sdelki_count,
                                               sdelok_sum=sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
    ##########################
    # all For Sochi
    #########################
    zero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, ).exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер','seo'])
    udl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*3, sdelok_sum__gt=1).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*3, sdelok_sum__gt=80000*3).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*3).order_by('-sdelok_sum').exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    ###########################
    # all For Adler
    ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    Audl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*3, sdelok_sum__gt=1,
                                                 auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*3, sdelok_sum__gt=80000*3,
                                                  auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*3,
                                                   auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    ##########################
    # reiting in otdel for nach otdel
    #########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*3, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*3, sdelok_sum__gt=80000*3, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*3, auth_group=gr).order_by('-sdelok_sum')
    ##########################
    # reiting in otdel for Golovin
    #########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел' or i.name == '2 Отдел' or i.name == '3 Отдел' or i.name == '4 Отдел':
            if i.name == 'Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum) + int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                s = reyt_sdelka_otd(otd=i.name, kommisia=sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    return render(request, 'crm/stat/sdelkareyting.html',
                  {'zero': zero_bal, 'udl': udl_bal, 'good': good_bal, 'great': great_bal,
                   'Azero': Azero_bal, 'Audl': Audl_bal, 'Agood': Agood_bal, 'Agreat': Agreat_bal,
                   'tn1': n1, 'tn2': n2, 'tn3': n3, 'tcrm_obj_week_count': crm_obj_week_count, 'tnach': nach_pr,
                   't_my_ya_obj': my_ya_obj, 'MForm': SearchMonthForm, 't11': Alsum,
                   'Nzero': Nzero_bal, 'Nudl': Nudl_bal, 'Ngood': Ngood_bal, 'Ngreat': Ngreat_bal, 'todtd': otd_reit})

#############################################
### Statistica po kol-vu objects & SDELKI
### 4 kvartal
############################################
@login_required
def reyting_po_sdelkam_4Kvartal_view(request):
    n1 = 'Рейтинг компании'
    date_end = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day)
    n2 ='C '+str(timezone.datetime.now().year)+'-01-01'+ ' по '+ str(timezone.datetime.now().year)+'-03-'+str(calendar.monthrange(timezone.datetime.now().year,1)[1])
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()

    if request.POST:
        form =  search_by_moth_form(request.POST)
        if form.is_valid():
            mothf = form.cleaned_data['month']
            mothf1 = form.cleaned_data['month']
            yearf = form.cleaned_data['year']
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'

            date_start = yearf+'-'+mothf+'-'+'01'
            date_end =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year,int(mothf))[1])
            n2 = 'c ' + date_start + 'по ' + date_end
            prizn = 1
            SearchMonthForm = search_by_moth_form(initial={'year': yearf, 'month': mothf1})
    else:
        date_start = str(timezone.datetime.now().year) + '-10-01'
        date_end = str(timezone.datetime.now().year) + '-12-' + str(
            calendar.monthrange(timezone.datetime.now().year, 12)[1])
        n2 = 'c ' + date_start + ' по ' + date_end +'(4 Квартал)'
        prizn = 3

        SearchMonthForm = search_by_moth_form()
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name == 'Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name = user.last_name + ' '+ user.first_name
                        sdelki_count = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start).count()
                        #################################################
                        ##### Kol _subj_Cian                            ###
                        #################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                          date_sozd__lte=date_end, date_sozd__gte=date_start).count()
                        #################################################
                        ##### Kol Subj CRM                            ###
                        #################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                            # date_sozd__lte=date_end, date_sozd__gte=date_start).count()

                        #################################################
                        ##### Summa Sdelok                            ###
                        #################################################
                        sdelki_sum = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start)
                        r_sum=0
                        rasr_sum1 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date__lte= date_end,
                                                             vneseno_komisii_date__gte=date_start)
                        if rasr_sum1:
                            rasr_sum1 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date__lte=date_end,
                                vneseno_komisii_date__gte=date_start).aggregate(Sum("vneseno_komisii"))
                            if rasr_sum1.get('vneseno_komisii__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii__sum') * 50 / 100))
                            else:
                                r_sum = r_sum
                        else:
                            r_sum=0

                        rasr_sum2 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date2__lte= date_end,
                                                             vneseno_komisii_date2__gte=date_start)
                        if rasr_sum2:
                            rasr_sum2 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date2__lte=date_end,
                                vneseno_komisii_date2__gte=date_start
                                ).aggregate(Sum("vneseno_komisii2"))
                            if rasr_sum2.get('vneseno_komisii2__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum2.get('vneseno_komisii2__sum') * 45 / 100))
                            else:
                                r_sum = r_sum


                        rasr_sum3 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date3__lte= date_end,
                                                             vneseno_komisii_date3__gte=date_start)
                        if rasr_sum3:
                            rasr_sum3 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date3__lte=date_end,
                                vneseno_komisii_date3__gte=date_start).aggregate(Sum("vneseno_komisii3"))
                            if rasr_sum3.get('vneseno_komisii3__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii3__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum4 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date4__lte= date_end,
                                                            vneseno_komisii_date4__gte=date_start)
                        if rasr_sum4:
                            rasr_sum4 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date4__lte=date_end,
                                vneseno_komisii_date4__gte=date_start).aggregate(Sum("vneseno_komisii4"))
                            if rasr_sum4.get('vneseno_komisii4__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii4__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum5 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date5__lte= date_end,
                                                             vneseno_komisii_date5__gte=date_start)
                        if rasr_sum5:
                            rasr_sum5 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date5__lte=date_end,
                                vneseno_komisii_date5__gte=date_start).aggregate(Sum("vneseno_komisii5"))
                            if rasr_sum5.get('vneseno_komisii5__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii5__sum') * 50 / 100))
                            else:
                                r_sum = r_sum

                        sum=0
                        sum = sum + int(r_sum)
                        for i in sdelki_sum:
                            if i.reelt1 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc1 / 100) * 2
                            if i.reelt2 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc2 / 100) * 2
                            if i.reelt3 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc3 / 100) * 2
                            if i.reelt4 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc4 / 100) * 2
                            if i.reelt5 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc5 / 100) * 2
                            if i.reelt6 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc6 / 100) * 2
                            if i.reelt7 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc7 / 100) * 2
                            if i.reelt8 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc8 / 100) * 2
                            if i.reelt9 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc9 / 100) * 2
                            if i.reelt10 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc10 / 100) * 2

                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name,
                                               sdelok_calc=sdelki_count,
                                               sdelok_sum=sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
    ##########################
    # all For Sochi
    #########################
    zero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, ).exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер','seo'])
    udl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn).order_by('-sdelok_sum').exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    ###########################
    # all For Adler
    ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    Audl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1,
                                                 auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn,
                                                  auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn,
                                                   auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    ##########################
    # reiting in otdel for nach otdel
    #########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn, auth_group=gr).order_by('-sdelok_sum')
    ##########################
    # reiting in otdel for Golovin
    #########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел' or i.name == '2 Отдел' or i.name == '3 Отдел' or i.name == '4 Отдел':
            if i.name == 'Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum) + int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                s = reyt_sdelka_otd(otd=i.name, kommisia=sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    return render(request, 'crm/stat/sdelkareyting.html',
                  {'zero': zero_bal, 'udl': udl_bal, 'good': good_bal, 'great': great_bal,
                   'Azero': Azero_bal, 'Audl': Audl_bal, 'Agood': Agood_bal, 'Agreat': Agreat_bal,
                   'tn1': n1, 'tn2': n2, 'tn3': n3, 'tcrm_obj_week_count': crm_obj_week_count, 'tnach': nach_pr,
                   't_my_ya_obj': my_ya_obj, 'MForm': SearchMonthForm, 't11': Alsum,
                   'Nzero': Nzero_bal, 'Nudl': Nudl_bal, 'Ngood': Ngood_bal, 'Ngreat': Ngreat_bal, 'todtd': otd_reit})

#############################################
### Statistica po kol-vu objects & SDELKI
### Tekushiy god
############################################
@login_required
def reyting_po_sdelkam_tek_god(request):
    n1 = 'Рейтинг компании'
    date_end = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day)
    n2 = 'текущий год'
    #3n2 ='C '+str(timezone.datetime.now().year)+'-01-01'+ ' по '+ str(timezone.datetime.now().year)+'-03-'+str(calendar.monthrange(timezone.datetime.now().year,1)[1])
    n3 = zayavka.objects.filter(status='Свободен').count()
    d11 = timezone.datetime.now().date() - timedelta(days=timezone.datetime.now().weekday())
    crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
    my_ya_obj = flat_obj.objects.filter(author=request.user).count()

    if request.POST:
        form =  search_by_moth_form(request.POST)
        if form.is_valid():
            mothf = form.cleaned_data['month']
            mothf1 = form.cleaned_data['month']
            yearf = form.cleaned_data['year']
            if mothf == 'Январь':
                mothf = '01'
            if mothf == 'Февраль':
                mothf = '02'
            if mothf == 'Март':
                mothf = '03'
            if mothf == 'Апрель':
                mothf = '04'
            if mothf == 'Май':
                mothf = '05'
            if mothf == 'Июнь':
                mothf = '06'
            if mothf == 'Июль':
                mothf = '07'
            if mothf == 'Август':
                mothf = '08'
            if mothf == 'Сентябрь':
                mothf = '09'
            if mothf == 'Октябрь':
                mothf = '10'
            if mothf == 'Ноябрь':
                mothf = '11'
            if mothf == 'Декабрь':
                mothf = '12'

            date_start = yearf+'-'+mothf+'-'+'01'
            date_end =  yearf+'-'+mothf+'-'+str(calendar.monthrange(timezone.datetime.now().year,int(mothf))[1])
            n2 = 'c ' + date_start + 'по ' + date_end
            prizn = 1
            SearchMonthForm = search_by_moth_form(initial={'year': yearf, 'month': mothf1})
    else:
        date_start = str(timezone.datetime.now().year) + '-01-01'
        date_end = str(timezone.datetime.now().year) + '-12-' + str(
            calendar.monthrange(timezone.datetime.now().year, 12)[1])
        n2 = 'c ' + date_start + ' по ' + date_end +'(4 Квартал)'
        #n2 = 'текущий год'
        prizn = 12

        SearchMonthForm = search_by_moth_form()
    reyting_po_sdelkam.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
            if (not user.groups.get().name == 'Администрация'):
                if (not user.groups.get().name == 'Юристы'):
                    if not user.groups.get().name == 'Офис-менеджер':
                        name = user.last_name + ' '+ user.first_name
                        sdelki_count = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start).count()
                        #################################################
                        ##### Kol _subj_Cian                            ###
                        #################################################
                        cian_counts = feed.objects.filter(author=user.id,
                                                          date_sozd__lte=date_end, date_sozd__gte=date_start).count()
                        #################################################
                        ##### Kol Subj CRM                            ###
                        #################################################
                        crm_counts = flat_obj.objects.filter(author=user.id,).count()
                                                            # date_sozd__lte=date_end, date_sozd__gte=date_start).count()

                        #################################################
                        ##### Summa Sdelok                            ###
                        #################################################
                        sdelki_sum = otchet_nov.objects.filter(
                            Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                            sdelka_zakrita='Да',
                            date_zakr__lte=date_end, date_zakr__gte=date_start)
                        r_sum=0
                        rasr_sum1 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date__lte= date_end,
                                                             vneseno_komisii_date__gte=date_start)
                        if rasr_sum1:
                            rasr_sum1 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date__lte=date_end,
                                vneseno_komisii_date__gte=date_start).aggregate(Sum("vneseno_komisii"))
                            if rasr_sum1.get('vneseno_komisii__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii__sum') * 45 / 100))
                            else:
                                r_sum = r_sum
                        else:
                            r_sum=0

                        rasr_sum2 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date2__lte= date_end,
                                                             vneseno_komisii_date2__gte=date_start)
                        if rasr_sum2:
                            rasr_sum2 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date2__lte=date_end,
                                vneseno_komisii_date2__gte=date_start
                                ).aggregate(Sum("vneseno_komisii2"))
                            if rasr_sum2.get('vneseno_komisii2__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum2.get('vneseno_komisii2__sum') * 45 / 100))
                            else:
                                r_sum = r_sum


                        rasr_sum3 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date3__lte= date_end,
                                                             vneseno_komisii_date3__gte=date_start)
                        if rasr_sum3:
                            rasr_sum3 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date3__lte=date_end,
                                vneseno_komisii_date3__gte=date_start).aggregate(Sum("vneseno_komisii3"))
                            if rasr_sum3.get('vneseno_komisii3__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii3__sum') * 45 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum4 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date4__lte= date_end,
                                                            vneseno_komisii_date4__gte=date_start)
                        if rasr_sum4:
                            rasr_sum4 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date4__lte=date_end,
                                vneseno_komisii_date4__gte=date_start).aggregate(Sum("vneseno_komisii4"))
                            if rasr_sum4.get('vneseno_komisii4__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii4__sum') * 45 / 100))
                            else:
                                r_sum = r_sum

                        rasr_sum5 = otchet_nov.objects.filter(Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                            | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(reelt7=user.username)
                            | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username), sdelka_zakrita='Рассрочка',
                                                             vneseno_komisii_date5__lte= date_end,
                                                             vneseno_komisii_date5__gte=date_start)
                        if rasr_sum5:
                            rasr_sum5 = otchet_nov.objects.filter(
                                Q(reelt1=user.username) | Q(reelt2=user.username) | Q(reelt3=user.username)
                                | Q(reelt4=user.username) | Q(reelt5=user.username) | Q(reelt6=user.username) | Q(
                                    reelt7=user.username)
                                | Q(reelt8=user.username) | Q(reelt9=user.username) | Q(reelt10=user.username),
                                sdelka_zakrita='Рассрочка',
                                vneseno_komisii_date5__lte=date_end,
                                vneseno_komisii_date5__gte=date_start).aggregate(Sum("vneseno_komisii5"))
                            if rasr_sum5.get('vneseno_komisii5__sum'):
                                r_sum = str(int(r_sum) + int(rasr_sum1.get('vneseno_komisii5__sum') * 45 / 100))
                            else:
                                r_sum = r_sum

                        sum=0
                        sum = sum + int(r_sum)
                        for i in sdelki_sum:
                            if i.reelt1 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc1 / 100) * 2
                            if i.reelt2 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc2 / 100) * 2
                            if i.reelt3 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc3 / 100) * 2
                            if i.reelt4 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc4 / 100) * 2
                            if i.reelt5 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc5 / 100) * 2
                            if i.reelt6 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc6 / 100) * 2
                            if i.reelt7 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc7 / 100) * 2
                            if i.reelt8 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc8 / 100) * 2
                            if i.reelt9 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc9 / 100) * 2
                            if i.reelt10 == user.username:
                                sum = sum + ((i.komisia / 2) * i.rielt_proc10 / 100) * 2

                        s = reyting_po_sdelkam(auth_nic=user.username, auth_group=user.groups.get(), auth_ful_name=name,
                                               sdelok_calc=sdelki_count,
                                               sdelok_sum=sum, cian_count=cian_counts, crm_count=crm_counts)
                        s.save()
    nach_pr = request.user.userprofile1.nach_otd
    ##########################
    # all For Sochi
    #########################
    zero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, ).exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер','seo'])
    udl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    good_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn).order_by(
        '-sdelok_sum').exclude(auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    great_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn).order_by('-sdelok_sum').exclude(
        auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    ###########################
    # all For Adler
    ###########################
    Azero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group__in=['Офис в Адлере', 'Администрация Адлер'])
    Audl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1,
                                                 auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn,
                                                  auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    Agreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn,
                                                   auth_group__in=['Офис в Адлере', 'Администрация Адлер']).order_by(
        '-sdelok_sum')
    ##########################
    # reiting in otdel for nach otdel
    #########################
    gr = request.user.groups.get().name
    Nzero_bal = reyting_po_sdelkam.objects.filter(sdelok_sum=0, auth_group=gr)
    Nudl_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=80000*prizn, sdelok_sum__gt=1, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngood_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__lte=120000*prizn, sdelok_sum__gt=80000*prizn, auth_group=gr).order_by(
        '-sdelok_sum')
    Ngreat_bal = reyting_po_sdelkam.objects.filter(sdelok_sum__gt=120000*prizn, auth_group=gr).order_by('-sdelok_sum')
    ##########################
    # reiting in otdel for Golovin
    #########################
    reyt_sdelka_otd.objects.all().delete()
    for i in Group.objects.all():
        if i.name == 'Офис в Адлере' or i.name == '1 Отдел' or i.name == '2 Отдел' or i.name == '3 Отдел' or i.name == '4 Отдел':
            if i.name == 'Офис в Адлере':
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                ASsum = reyting_po_sdelkam.objects.filter(auth_group='Администрация Адлер').aggregate(Sum('sdelok_sum'))
                Alsum = str(ASsum.get('sdelok_sum__sum'))
                if str(Alsum) == 'None':
                    AlSum = 0
                AllSum = int(sum) + int(Alsum)

                s = reyt_sdelka_otd(otd=i.name, kommisia=AllSum)
                s.save()
            else:
                Ssum = reyting_po_sdelkam.objects.filter(auth_group=i.name).aggregate(Sum('sdelok_sum'))
                sum = str(Ssum.get('sdelok_sum__sum'))
                s = reyt_sdelka_otd(otd=i.name, kommisia=sum)
                s.save()
    otd_reit = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    return render(request, 'crm/stat/sdelkareyting.html',
                  {'zero': zero_bal, 'udl': udl_bal, 'good': good_bal, 'great': great_bal,
                   'Azero': Azero_bal, 'Audl': Audl_bal, 'Agood': Agood_bal, 'Agreat': Agreat_bal,
                   'tn1': n1, 'tn2': n2, 'tn3': n3, 'tcrm_obj_week_count': crm_obj_week_count, 'tnach': nach_pr,
                   't_my_ya_obj': my_ya_obj, 'MForm': SearchMonthForm, 't11': Alsum,
                   'Nzero': Nzero_bal, 'Nudl': Nudl_bal, 'Ngood': Ngood_bal, 'Ngreat': Ngreat_bal, 'todtd': otd_reit})

##########################################################
## Otchet po kachestvu obj (5 pict, numb kv, 300 simvolov
###########################################################
def kach_otch_view(request):
    n1='Качество'
    n2='Обьявлений'
    n3 = zayavka.objects.filter(status='Свободен').count()
    #"""""
    for i in flat_obj.objects.all():

        if i.kvart_numb:
            i.kv_err='False'
        else:
            i.kv_err = 'True'
        if i.dom_numb or i.kadastr:
            i.dom_err='False'
        else:
            i.dom_err='True'
        if len(i.prim)<300:
            i.text_err='True'
        else:
            i.text_err='False'
        if i.idd_gal.count()<3:
            i.pict_err='True'
        else:
            i.pict_err='False'
        i.save()
        cachestvoDomCl.objects.all().delete()
   # """
    cachestvoDomCl.objects.all().delete()
    for user in User.objects.all():
        if user.is_active:
           if (not user.groups.get().name == 'Администрация'):
              if (not user.groups.get().name == 'Юристы'):
                  if not user.groups.get().name == 'Офис-менеджер':
                            tFIO = user.last_name +' '+ user.first_name
                            totdel = user.groups.get().name
                            al_count = flat_obj.objects.filter(Q (author=user.id)).count()
                            text_count = flat_obj.objects.filter(author=user.id, text_err='True').count()
                            kv_count = flat_obj.objects.filter(author=user.id, kv_err='True').count()
                            dom_count = flat_obj.objects.filter(author=user.id, dom_err='True').count()
                            pc_count = flat_obj.objects.filter(author=user.id, pict_err='True').count()
                            s= cachestvoDomCl(FIO=tFIO, otdel=totdel, vsego=al_count, text_err=text_count,
                                              kv_numb_err=kv_count, photo_err =pc_count,
                                              dom_numb_err = dom_count)
                            s.save()

    totdel = request.user.groups.get().name
    if request.user.userprofile1.nach_otd == 'Да' or request.user.groups.get().name=='Администрация' or request.user.groups.get().name=='Администрация Адлер':
        if request.user.groups.get().name == 'Администрация':
            post = cachestvoDomCl.objects.filter(vsego__gt = 0).order_by('otdel')
        if request.user.userprofile1.nach_otd == 'Да' and not request.user.groups.get().name == 'Администрация':
            post = cachestvoDomCl.objects.filter(vsego__gt = 0, otdel = totdel).order_by('otdel')
        if request.user.groups.get().name == 'Администрация Адлер':
            post = cachestvoDomCl.objects.filter(vsego__gt = 0, otdel='Офис в Адлере').order_by('otdel')
    else:
        post = cachestvoDomCl.objects.filter(vsego__lt=0, otdel=totdel).order_by('otdel')

    all = flat_obj.objects.all().count()
    good = flat_obj.objects.filter(text_err='False', kv_err='False', pict_err='False', dom_err='False').count()
    bad = flat_obj.objects.filter(Q(text_err='True')| Q(kv_err='True') | Q(pict_err='True')|
                                   Q(dom_err='True')).count()
    if auth.get_user(request).username =='homka':
        n2=n2+' Всего:'+str(all)+' Без обшибок:'+str(good)+' C ошибками:'+str(bad)
    return render(request, 'crm/stat/KachDMCkl.html',{'tn1':n1, 'tn2':n2,'tpost':post, 'tall':all, 'tgood':good, 'tbad':bad})



@login_required
def my_admi_view(request):
    ########################
    ## For yandex
    ########################
    atoken = 'AQAAAAAL3YMmAAUP5ttpdkGLCkoSkUQM4FKV7AE'
    y11 = str(timezone.datetime.now().strftime('%Y-%m-%d'))
    d1 = requests.get(
        'https://api-metrika.yandex.ru/stat/v1/data?&id=46923189&accuracy=full&date1=' + y11 + '&date2=' + y11 + '&metrics=ym:s:visits&oauth_token=' + atoken)
    parsed1 = json.loads(d1.text)
    #pars_param = parsed1['data'][0]['metrics'][0]
    pars= parsed1
    n1='CRM' #+ ' pars with params='#+ str(pars_param)
    #n2='администрирование'+' pars='+str(pars)
    n2='pars='+str(pars)
    del1='1'
############################################################
## Start of Vetsum
############################################################
    vsForm = vestum_count_form()
    PrVsForm = vestum_poryadok_form()
    all_reelt = User.objects.filter(is_active=True).exclude(groups__in=['8', '9', '10','12','11','13'])\
        .order_by('groups__name', 'last_name')
############################################################
## End of Vetsum
############################################################
    if request.POST:
        if 'cian_delete' in request.POST:
            f = adm_form(request.POST)
            if f.is_valid():
                all_reelt = User.objects.filter(is_active=True).exclude(groups__in=['8', '9', '10', '12', '11', '13']) \
                    .order_by('groups__name', 'last_name')
                d1 = f.cleaned_data['st_date']
                d2 = f.cleaned_data['end_date']
                cian = feed.objects.filter(date_sozd__gt=d1, date_sozd__lte=d2)
                del1 =str(cian.count())
                cian.delete()
                cian = feed_gallery.objects.filter(date__gt=d1, date__lte=d2)
                cian.delete()
                form = adm_form(initial={'st_date': d1, 'end_date': d2})
                return render(request, 'any/my_adm.html', {'tn1': n1, 'tn2': n2, 'tform': form, 'tdel': del1,
                                                           'tPrVsForm':PrVsForm,'tVsForm':vsForm,'tallreelt':all_reelt,})

        if 'vestumAdd' in request.POST:
            f = vestum_count_form(request.POST)
            if f.is_valid():
                vsForm = vestum_count_form()
                balls = f.cleaned_data['vs_count']
                form = adm_form()
                all_reelt = User.objects.filter(is_active=True).exclude(groups__in=['8', '9', '10', '12', '11', '13']) \
                    .order_by('groups__name', 'last_name')
                for usr in UserProfile1.objects.all():
                    usr.vestum_count_ads = int(balls)
                    usr.save()
                return render(request, 'any/my_adm.html', {'tn1': n1, 'tn2': n2, 'tform': form, 'tdel': del1,
                                                           'tPrVsForm':PrVsForm,'tVsForm':vsForm, 'tallreelt':all_reelt,})




    #else:
    form = adm_form()
    return render(request,'any/my_adm.html',{'tn1':n1, 'tn2':n2,'tform':form,'tdel':del1, 'tVsForm':vsForm,
                                             'tPrVsForm':PrVsForm, 'tallreelt':all_reelt})
@login_required
def DashBoardView(request):
    ########################
    ## Start Users count
    ########################
    AllUsr = User.objects.filter(is_active='1').exclude(groups__in=['8', '9', '10','12','11','13']).count()
    ########################
    ## End Users count
    ########################
    n1='CRM'
    n2='Основные показатели; '+str(AllUsr)+' Сотрудников'
    ########################
    ## For yandex
    ########################
    atoken = 'AQAAAAAL3YMmAAUP5ttpdkGLCkoSkUQM4FKV7AE'
    y11 = str(timezone.datetime.now().strftime('%Y-%m-%d'))
    y12 = str((timezone.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
    y13 = str((timezone.datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'))
    y14 = str((timezone.datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'))
    d1 = requests.get(
        'https://api-metrika.yandex.ru/stat/v1/data?&id=46923189&accuracy=full&date1=' + y11 + '&date2=' + y11 + '&metrics=ym:s:visits&oauth_token=' + atoken)
    d2 = requests.get(
        'https://api-metrika.yandex.ru/stat/v1/data?&id=46923189&accuracy=full&date1=' + y12 + '&date2=' + y12 + '&metrics=ym:s:visits&oauth_token=' + atoken)
    d3 = requests.get(
        'https://api-metrika.yandex.ru/stat/v1/data?&id=46923189&accuracy=full&date1=' + y13 + '&date2=' + y13 + '&metrics=ym:s:visits&oauth_token=' + atoken)
    d4 = requests.get(
        'https://api-metrika.yandex.ru/stat/v1/data?&id=46923189&accuracy=full&date1=' + y14 + '&date2=' + y14 + '&metrics=ym:s:visits&oauth_token=' + atoken)
    parsed1 = json.loads(d1.text)
    parsed2 = json.loads(d2.text)
    parsed3 = json.loads(d3.text)
    parsed4 = json.loads(d4.text)
    if parsed1['data']:
        c1 = parsed1['data'][0]['metrics'][0]
    #if c1 == 'ym:s:visits':
    else:
        c1 = 0
    c2 = parsed2['data'][0]['metrics'][0]
    c3 = parsed3['data'][0]['metrics'][0]
    c4 = parsed4['data'][0]['metrics'][0]
    ########################
    ## End for yandex
    ########################
    ########################
    ## End for Domclik
    ########################
    dmAllCount = flat_obj.objects.filter(kadastr='', type='flat').count()
    dmCadastrCount = flat_obj.objects.filter(type='flat')#.exclude(kadastr='').count()
    dmCadastrCount = dmCadastrCount.exclude(kadastr='').count()
    dmaAll = dmCadastrCount+dmAllCount
    ########################
    ## End for Domcklick
    ########################
    ########################
    ## for Cian
    ########################
    date= datetime.now() - timedelta(days=10)
    #post = feed.objects.filter(pub='Да', date_sozd__gte=date).order_by('-date_sozd')[:600]
    cn = get_object_or_404(TmpCianCount, pk=1)
    tsochi = cn.sochi
    tadler = cn.adler
    count = feed.objects.filter(pub='Да', date_sozd__gte=date).exclude( author__groups__name='Офис в Адлере').count()
    post = feed.objects.filter(pub='Да', date_sozd__gte=date).exclude( author__groups__name='Офис в Адлере').order_by(
        '-date_sozd')[:tsochi]
    if count < tsochi:
        apost = feed.objects.filter(pub='Да', date_sozd__gte=date,  author__groups__name='Офис в Адлере').order_by(
            '-date_sozd')[:tadler+(tsochi-count)]
    else:
        apost = feed.objects.filter(pub='Да', date_sozd__gte=date,  author__groups__name='Офис в Адлере').order_by(
            '-date_sozd')[:tadler]
    cianSochi = post.count()
    cianAdler = apost.count()
    cianAll= cianSochi+cianAdler
    ########################
    ## End for Cian
    ########################
    ########################
    ## Start for All Pribil
    ########################
    ds = fdate = str(timezone.datetime.now().year) + '-' + str(timezone.datetime.now().month) + '-' + '01'
    de = str(timezone.datetime.now().year) + '-' + str(timezone.datetime.now().month) + '-' + str(
        timezone.datetime.now().day)
    open_otchet = otchet_nov.objects.filter(sdelka_zakrita='Нет').order_by('-date_sozd', '-pk')

    #sum_adler = otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, adler_pr='Адлер', \
    #                                      sdelka_zakrita='Да').aggregate(Sum("komisia"))
    sum_adler = otchet_nov.objects.filter(Q (otd_reelt1='Администрация Адлер') | Q (otd_reelt1='Офис в Адлере')
                                          | Q (otd_reelt2='Офис в Адлере') | Q (otd_reelt2='Администрация Адлер')
                                          | Q(otd_reelt3='Офис в Адлере') | Q(otd_reelt3='Администрация Адлер')
                                          | Q(otd_reelt4='Офис в Адлере') | Q(otd_reelt4='Администрация Адлер')
                                          | Q(otd_reelt5='Офис в Адлере') | Q(otd_reelt5='Администрация Адлер')
                                          | Q(otd_reelt6='Офис в Адлере') | Q(otd_reelt6='Администрация Адлер')
                                          | Q(otd_reelt7='Офис в Адлере') | Q(otd_reelt7='Администрация Адлер')
                                          | Q(otd_reelt8='Офис в Адлере') | Q(otd_reelt8='Администрация Адлер')
                                          | Q(otd_reelt9='Офис в Адлере') | Q(otd_reelt9='Администрация Адлер')
                                          | Q (otd_reelt10='Офис в Адлере') | Q (otd_reelt10='Администрация Адлер'),
                                          date_zakr__gte=ds, date_zakr__lte=de, sdelka_zakrita='Да',).aggregate(Sum("komisia"))

    #sum_sochi = otchet_nov.objects.filter(date_zakr__gte=ds, date_zakr__lte=de, adler_pr='',
    #                                      sdelka_zakrita='Да').aggregate(Sum("komisia"))
    grp = 'Отдел'
    sum_sochi = otchet_nov.objects.filter(
        Q(otd_reelt1__contains=grp) | Q(otd_reelt2__contains=grp) | Q(otd_reelt3__contains=grp)
        | Q(otd_reelt4__contains=grp) | Q(otd_reelt5__contains=grp) | Q(otd_reelt6__contains=grp) | Q(
            otd_reelt7__contains=grp)
        | Q(otd_reelt8__contains=grp) | Q(otd_reelt9__contains=grp) | Q(otd_reelt10__contains=grp), date_zakr__gte=ds,
        date_zakr__lte=de,
        sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum_sochi.get('komisia__sum'):
        s_sochi = str(sum_sochi.get('komisia__sum') * 45 / 100)
    else:
        s_sochi = '0'

    if sum_adler.get('komisia__sum'):
        s_adler = str(sum_adler.get('komisia__sum') * 45 / 100)
    else:
        s_adler = '0'
    ########################
    ## End for All pribil
    ########################
    ########################
    ## Start for Reiting
    ########################
    rOtd = reyt_sdelka_otd.objects.all().order_by('-kommisia')
    sOtd = reyting_po_sdelkam.objects.all().exclude(auth_group='Офис в Адлере').exclude(
        auth_group='Администрация Адлер').order_by('-sdelok_sum')[:5]
    aOtd = reyting_po_sdelkam.objects.all().exclude(auth_group='1 Отдел').exclude(
        auth_group='2 Отдел').exclude(auth_group='3 Отдел').exclude(auth_group='4 Отдел').order_by('-sdelok_sum')[:5]
    ########################
    ## End for Reiting
    ########################
    ########################
    ## Start for month pribil
    ########################
    ds1 = timezone.datetime.now() - timedelta(days=timezone.datetime.now().day-1)
    de1 = timezone.datetime.now()
    dm1 = str(de1.day)+'-'+str(de1.month)+'-'+str(de1.year)
    tds2 = ds1 - timedelta(days=1)
    ds2 = ds1 - timedelta(days=tds2.day)
    de2 = ds1 - timedelta(days=1)
    dm2 = str(de2.day) + '-' + str(de2.month) + '-' + str(de2.year)
    tds3 = ds2 - timedelta(days=1)
    ds3 = ds2 - timedelta(days=tds3.day)
    de3 = ds2 - timedelta(days=1)
    dm3 = str(de3.day) + '-' + str(de3.month) + '-' + str(de3.year)
    tds4 = ds3 - timedelta(days=1)
    ds4 = ds3 - timedelta(days=tds4.day)
    de4 = ds3 - timedelta(days=1)
    dm4 = str(de4.day) + '-' + str(de4.month) + '-' + str(de4.year)
    tds5 = ds4 - timedelta(days=1)
    ds5 = ds4 - timedelta(days=tds5.day)
    de5 = ds4 - timedelta(days=1)
    dm5 = str(de5.day) + '-' + str(de5.month) + '-' + str(de5.year)
    tds6 = ds5 - timedelta(days=1)
    ds6 = ds5 - timedelta(days=tds6.day)
    de6 = ds5 - timedelta(days=1)
    dm6 = str(de6.day) + '-' + str(de6.month) + '-' + str(de6.year)
    sum = otchet_nov.objects.filter(date_zakr__gte=ds1, date_zakr__lte=de1, sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum.get('komisia__sum'):
        s_sochi_m1 = str(sum.get('komisia__sum') * 45 / 100)
    else:
        s_sochi_m1 = '0'
    sum = otchet_nov.objects.filter(date_zakr__gte=ds2, date_zakr__lte=de2, sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum.get('komisia__sum'):
        s_sochi_m2 = str(sum.get('komisia__sum') * 45 / 100)
    else:
        s_sochi_m2 = '0'
    sum = otchet_nov.objects.filter(date_zakr__gte=ds3, date_zakr__lte=de3, sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum.get('komisia__sum'):
        s_sochi_m3 = str(sum.get('komisia__sum') * 45 / 100)
    else:
        s_sochi_m3 = '0'
    sum = otchet_nov.objects.filter(date_zakr__gte=ds4, date_zakr__lte=de4, sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum.get('komisia__sum'):
        s_sochi_m4 = str(sum.get('komisia__sum') * 45 / 100)
    else:
        s_sochi_m4 = '0'
    sum = otchet_nov.objects.filter(date_zakr__gte=ds5, date_zakr__lte=de5, sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum.get('komisia__sum'):
        s_sochi_m5 = str(sum.get('komisia__sum') * 45 / 100)
    else:
        s_sochi_m5 = '0'
    sum = otchet_nov.objects.filter(date_zakr__gte=ds6, date_zakr__lte=de6, sdelka_zakrita='Да').aggregate(Sum("komisia"))
    if sum.get('komisia__sum'):
        s_sochi_m6 = str(sum.get('komisia__sum') * 45 / 100)
    else:
        s_sochi_m6 = '0'
    ########################
    ## end for month pribil
    ########################
    ########################
    ## Start for stat buy objects
    ########################
    studia_count = flat_obj.objects.filter(type = 'flat', komnat ='Студия').count()
    OneRoom_count = flat_obj.objects.filter(type = 'flat', komnat='Однокомнатная').count()
    OneRoom_Sum = flat_obj.objects.filter(type = 'flat', komnat='Однокомнатная').aggregate(Sum("cena_agenstv"))
    OneRoomSrCena = int(str(OneRoom_Sum.get('cena_agenstv__sum'))) // OneRoom_count

    TwoRoom_count  = flat_obj.objects.filter(type = 'flat', komnat ='Двухкомнатная').count()
    TwoRoom_Sum = flat_obj.objects.filter(type = 'flat', komnat='Двухкомнатная').aggregate(Sum("cena_agenstv"))
    TwoRoomSrCena = int(str(OneRoom_Sum.get('cena_agenstv__sum'))) // TwoRoom_count

    TreeRoom_count  = flat_obj.objects.filter(type = 'flat', komnat='Трехкомнатная').count()
    TreeRoom_Sum = flat_obj.objects.filter(type = 'flat', komnat='Трехкомнатная').aggregate(Sum("cena_agenstv"))
    TreeRoomSrCena = int(str(OneRoom_Sum.get('cena_agenstv__sum'))) // TreeRoom_count

    ManyRoom_count  = flat_obj.objects.filter(type = 'flat', komnat='Многокомнатная').count()
    Houses_count = flat_obj.objects.filter(type = 'house').count()
    all_count = studia_count + OneRoom_count + TwoRoom_count + TreeRoom_count + ManyRoom_count + Houses_count
    ########################
    ## end for stat buy objects
    ########################
    return render(request,'crm/stat/dashboard.html',{'tn1':n1, 'tn2':n2, 'tcianA':cianAdler, 'tCianS':cianSochi,
                                                     'tc': c1, 'y': y11, 'tc2': c2, 'y2': y12, 'tc3': c3, 'y3': y13,
                                                     'tc4': c4, 'y4': y14, 'tdmall':dmAllCount, 'tdmcadastr':dmCadastrCount,
                                                     'tcianAll':cianAll,'tdmAll':dmaAll, 'trOtd':rOtd, 'tsOtd':sOtd,'taOtd':aOtd,
                                                     'tssochi':s_sochi, 'tsadler':s_adler,
                                                     'tdsum1':s_sochi_m1, 'tdsum2':s_sochi_m2, 'tdsum3':s_sochi_m3,
                                                     'tdsum4': s_sochi_m4, 'tdsum5':s_sochi_m5, 'tdsum6':s_sochi_m6,
                                                     'tdm1':dm1,'tdm2': dm2,'tdm3':dm3,'tdm4':dm4,'tdm5':dm5,'tdm6':dm6,
                                                     'tstcount':studia_count,'tonecount':OneRoom_count,
                                                     'ttwo_count':TwoRoom_count, 'ttreecount':TreeRoom_count,
                                                     'tmanycount':ManyRoom_count,'thouse_count':Houses_count,'tAllCount':all_count,
                                                     'tOneCrs': OneRoomSrCena, 'tTwoCrs': TwoRoomSrCena,'tTreCrs': TreeRoomSrCena,})

