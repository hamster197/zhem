from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from crm.models import UserProfile1, rielt_proc
from datetime import timezone, datetime, timedelta
import calendar

from .forms import loginform, chpassform

def login_view(request):
    if request.user.is_authenticated:
        return redirect('crm:news_index')
    else:
        if request.POST:
            form=loginform(request.POST)
            if form.is_valid():
                u=form.cleaned_data['username']
                p=form.cleaned_data['passw']
                user=authenticate(username = u , password = p)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        id = request.user.pk
                        us = get_object_or_404(UserProfile1, pk =id)
                        us.search_minc = 0
                        us.search_maxc = 100000000
                        us.search_minp = 0
                        us.search_maxp = 1000
                        us.search_raion = 'Любой'
                        us.save()
                        now = datetime.now()
                        d_start = datetime(datetime.now().year, 1, 1)
                        d_end = datetime(datetime.now().year, 3,
                                         calendar.monthrange(datetime.now().year, 3)[1])
                        if now > d_start and now < d_end:
                            kv = '1 Квартал'
                        d_start = datetime(datetime.now().year, 3, 1)
                        d_end = datetime(datetime.now().year, 6,
                                         calendar.monthrange(datetime.now().year, 6)[1])
                        if now > d_start and now < d_end:
                            kv = '2 Квартал'
                        d_start = datetime(datetime.now().year, 6, 1)
                        d_end = datetime(datetime.now().year, 9,
                                         calendar.monthrange(datetime.now().year, 9)[1])
                        if now > d_start and now < d_end:
                            kv = '3 Квартал'
                        d_start = datetime(datetime.now().year, 9, 1)
                        d_end = datetime(datetime.now().year, 12,
                                         calendar.monthrange(datetime.now().year, 12)[1])
                        if now > d_start and now < d_end:
                            kv = '4 Квартал'

                        if rielt_proc.objects.filter(year=datetime.now().year).count() == 0:
                            for usr in User.objects.filter(is_active=True):
                                s = rielt_proc(id_rielt_id=usr.id, kvartal=kv, year=datetime.now().year)
                                s.save()
                        if request.user.groups.get().name == 'Администрация':
                            return redirect('crm:DashBoard')
                        else:
                            return redirect('crm:news_index')


        else:
            form=loginform()
    return render(request,'crm/login.html',{'tpform':form})

def v404_view(request):
    if request.user.is_authenticated:
        if request.user.groups.get().name == 'Администрация':
            return redirect('crm:DashBoard')
        else:
            return redirect('crm:news_index')
    else:
        form=loginform()
    return render(request,'crm/login.html',{'tpform':form})

@login_required
def ch_pass_view(request):
    n1='Пароль'
    n2='смена'
    if request.POST:
        form=chpassform(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data['ps1']
            p2 = form.cleaned_data['ps2']
            if p1==p2:

                u = User.objects.get(username__contains=request.user)
                u.set_password(p1)
                u.save()
                return redirect('crm:news_index')
    else:
        form=chpassform()
    return render(request, 'crm/ch_pass_tmp.html', {'tpform':form,'tn1':n1,'tn2':n2})