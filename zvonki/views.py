from datetime import timezone, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from zvonki.models import zvonok
from django.forms import modelformset_factory,  Textarea
from datetimepicker.widgets import DateTimePicker

##################
# index of zvonki
##################

@login_required
def zv_index_view(request):
    n1='CRM'
    n2 ='222'
    nzvn = modelformset_factory(zvonok, fields=('tel', 'client_name', 'subj', 'cena', 'status_zvonka',
                                                'prezvonit', 'coment', ),
                                        widgets={'prezvonit':  DateTimePicker(options={'format': '%Y-%m-%d %H:%M',
	                                            'language': 'ru-ru',}),
                                            'coment': Textarea(attrs={'rows': 80, 'cols': 20})},
                                        extra=1,)
    nzvn_formset = nzvn(queryset=zvonok.objects.all())
    if request.POST:
        nformset = nzvn(request.POST,request.FILES)
        if nformset.is_valid():
            nformset.save()
    return render(request,'zvonki/index.html',{'tn1':n1,'tn2':n2, 'nformset':nzvn_formset })


@login_required
def pr_status_zvn_view(request, idd):
    zvn = get_object_or_404(zvonok , pk = idd)
    zvn.status_zvonka = 'Перезвонить'
    zvn.save()
    return redirect('zvn:index')

@login_required
def nd_status_zvn_view(request, idd):
    zvn = get_object_or_404(zvonok , pk = idd)
    zvn.status_zvonka = 'Недозвонился'
    zvn.save()
    return redirect('zvn:index')

@login_required
def work_status_zvn_view(request, idd):
    zvn = get_object_or_404(zvonok , pk = idd)
    zvn.status_zvonka = 'В работе'
    zvn.save()
    return redirect('zvn:index')

@login_required
def arh_status_zvn_view(request, idd):
    zvn = get_object_or_404(zvonok , pk = idd)
    zvn.status_zvonka = 'Архив'
    zvn.save()
    return redirect('zvn:index')

@login_required
def for_all_status_zvn_view(request, idd):
    zvn = get_object_or_404(zvonok , pk = idd)
    zvn.status_zvonka = 'В общем доступе'
    zvn.save()
    return redirect('zvn:index')
