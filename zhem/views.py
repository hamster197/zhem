from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from crm.models import UserProfile1

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