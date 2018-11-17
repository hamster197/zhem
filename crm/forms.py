
from django.utils import timezone
from material import *
from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectMultiple

from .models import news, flat_obj, flat_obj_gal, clients, uchastok, otchet_nov, feed, feed_gallery, zayavka, \
    UserProfile1, domclickText, vestum_poryadok_feed


class loginform(forms.Form):
    username=forms.CharField(max_length=20, label='Имя пользователя1')
    passw=forms.CharField(max_length=10,widget=forms.PasswordInput, label='Пароль')

class newsform(forms.ModelForm):
    class Meta:
        model=news
        fields=('nazv','text')



############################3
#FLATS
############################

class flatform(forms.ModelForm):
    class Meta:
        model=flat_obj
        fields=('exclusiv','client_name','client_tel','adress','raion','dom_numb','kvart_numb','kvart_numb','etap_sdachi','status_gilya','klass_gilya',
                'remont','gaz','komnat','ploshad','etag','etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv',
                'security','rubbish_chute','lift','balcony', 'prim','domclick_pub')
        #fields=('client_name','client_tel','status_obj','adress','raion','etap_sdachi','status_gilya','klass_gilya','remont','gaz','komnat','ploshad','etag','etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv','prim')
    def clean(self):
        cleaned_data = super(flatform, self).clean()
        if str(cleaned_data['etag'])=='0' or str(cleaned_data['etagnost'])=='0':
                raise ValidationError('Этаж или Этажность равны 0!' , code='invalid')
        if int(cleaned_data['etag'])>int(cleaned_data['etagnost']):
                raise ValidationError('Этаж больше этажности' , code='invalid')
        if str(cleaned_data['kvart_numb'])=='' and str(cleaned_data['kadastr'])=='':
                raise ValidationError('введите №кв или кадастр' , code='invalid')
        if len(str(cleaned_data['prim'])) < 300:
                raise ValidationError('меньше 300 символов в описании' , code='invalid')
        if  str(cleaned_data['raion'])=='Выбор района':
                raise ValidationError('Не выбран район!' , code='invalid')
        return cleaned_data

class flatform_appart(forms.ModelForm):
    class Meta:
        model=flat_obj
        fields=('exclusiv','client_name','client_tel','adress','raion','dom_numb','kvart_numb','kvart_numb','etap_sdachi','klass_gilya',
                'remont','gaz','komnat','ploshad','etag','etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv',
                'security','rubbish_chute','lift','balcony', 'prim','domclick_pub')
        #fields=('client_name','client_tel','status_obj','adress','raion','etap_sdachi','status_gilya','klass_gilya','remont','gaz','komnat','ploshad','etag','etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv','prim')
    def clean(self):
        cleaned_data = super(flatform_appart, self).clean()
        if str(cleaned_data['etag'])=='0' or str(cleaned_data['etagnost'])=='0':
                raise ValidationError('Этаж или Этажность равны 0!' , code='invalid')
        if int(cleaned_data['etag'])>int(cleaned_data['etagnost']):
                raise ValidationError('Этаж больше этажности' , code='invalid')
        if str(cleaned_data['kvart_numb'])=='' and str(cleaned_data['kadastr'])=='':
                raise ValidationError('введите №кв или кадастр' , code='invalid')
        if len(str(cleaned_data['prim'])) < 300:
                raise ValidationError('меньше 300 символов в описании' , code='invalid')
        if  str(cleaned_data['raion'])=='Выбор района':
                raise ValidationError('Не выбран район!' , code='invalid')
        return cleaned_data


class resep_flatform(forms.ModelForm):
    class Meta:
        model=flat_obj
        fields=('author','client_tel','client_name','adress','raion','dom_numb','kvart_numb','cena_agenstv',)
    def clean(self):
        cleaned_data = super(resep_flatform, self).clean()
        if str(cleaned_data['kvart_numb'])=='':
                raise ValidationError('введите №кв' , code='invalid')
        if  str(cleaned_data['raion'])=='Выбор района':
                raise ValidationError('Не выбран район!' , code='invalid')
        return cleaned_data

class kadastr_form(forms.ModelForm):
    class Meta:
        model = flat_obj
        fields = ('kadastr',)


class yandex_flatform(forms.ModelForm):
    class Meta:
        model=flat_obj#'kredit',
        fields=('exclusiv','client_name','client_tel','adress','dom_numb','kvart_numb','raion',
                'etap_sdachi','status_gilya','klass_gilya','remont','gaz','komnat','ploshad','etag',
                'etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv','prim',
                'security','rubbish_chute','lift','balcony','domclick_pub')
        #fields=('client_name','client_tel','domclick','status_obj','adress','raion','etap_sdachi','status_gilya','klass_gilya','remont','gaz','komnat','ploshad','etag','etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv','prim')
    def clean(self):
        cleaned_data = super(yandex_flatform, self).clean()
        if str(cleaned_data['etag']) == '0' or str(cleaned_data['etagnost']) == '0':
                raise ValidationError('Этаж или Этажность равны 0!' , code='invalid')
        if int(cleaned_data['etag'])>int(cleaned_data['etagnost']):
                raise ValidationError('Этаж больше этажности' , code='invalid')
        if str(cleaned_data['kvart_numb']) == '' and str(cleaned_data['kadastr']) == '':
                raise ValidationError('введите №кв или кадастр' , code='invalid')
        if len(str(cleaned_data['prim'])) == 0:
                raise ValidationError('Введите текст описания' , code='invalid')
        if len(str(cleaned_data['prim'])) < 300:
                raise ValidationError('меньше 300 символов в описании' , code='invalid')
        if  str(cleaned_data['raion'])=='Выбор района':
                raise ValidationError('Выберите район!' , code='invalid')

        return cleaned_data



class flateditform(forms.ModelForm):
    class Meta:
        model=flat_obj#'kredit',
        fields=('adress','dom_numb','kvart_numb','etap_sdachi','status_gilya','klass_gilya','remont',
                'komnat','ploshad','etag','etagnost','vid_is_okon','san_usel','parking','kadastr',
                'cena_sobstv','cena_agenstv','prim','security','rubbish_chute','lift','balcony','domclick_pub')
    def clean(self):
        cleaned_data = super(flateditform, self).clean()
        if str(cleaned_data['etag']) == '0' or str(cleaned_data['etagnost']) == '0':
                raise ValidationError('Этаж или Этажность равны 0!' , code='invalid')
        if int(cleaned_data['etag'])>int(cleaned_data['etagnost']):
                raise ValidationError('Этаж больше этажности' , code='invalid')
        if str(cleaned_data['kvart_numb']) == '' and str(cleaned_data['kadastr']) == '':
                raise ValidationError('введите №кв или кадастр' , code='invalid')
        if len(str(cleaned_data['prim'])) == 0:
                raise ValidationError('Введите текст описания' , code='invalid')
        if len(str(cleaned_data['prim'])) < 300:
                raise ValidationError('меньше 300 символов в описании' , code='invalid')
        if str(cleaned_data['dom_numb']) == '':
                raise ValidationError('Нет номера дома' , code='invalid')
        return cleaned_data

class vestum_pub_form(forms.ModelForm):
    class Meta:
        model = flat_obj
        fields =('nov_nazv',)
    def clean(self):
        cleaned_data = super(vestum_pub_form, self).clean()
        if str(cleaned_data['nov_nazv']) == '':
                raise ValidationError('Нет названия дома!' , code='invalid')
        return cleaned_data

class yandex_flateditform(forms.ModelForm):
    class Meta:
        model=flat_obj#'kredit',
        fields=('adress','dom_numb','domclick','adress','dom_numb','kvart_numb','kvart_numb',
                'etap_sdachi','status_gilya','klass_gilya','remont','gaz','komnat','ploshad','etag',
                'etagnost','vid_is_okon','san_usel','parking','kadastr','cena_sobstv','cena_agenstv','prim',
                'security','rubbish_chute','lift','balcony','domclick_pub')
    def clean(self):
        cleaned_data = super(yandex_flateditform, self).clean()
        if str(cleaned_data['etag']) == '0' or str(cleaned_data['etagnost']) == '0':
                raise ValidationError('Этаж или Этажность равны 0!' , code='invalid')
        if int(cleaned_data['etag'])>int(cleaned_data['etagnost']):
                raise ValidationError('Этаж больше этажности' , code='invalid')
        if str(cleaned_data['kvart_numb']) == '' and str(cleaned_data['kadastr']) == '':
                raise ValidationError('введите №кв или кадастр' , code='invalid')
        if len(str(cleaned_data['prim'])) < 300:
                raise ValidationError('меньше 300 символов в описании' , code='invalid')
        if str(cleaned_data['dom_numb']) == '':
                raise ValidationError('Нет номера дома' , code='invalid')
        return cleaned_data

raion_choises = (('Ареда','Ареда'),('Ахун', 'Ахун'),('Бытха', 'Бытха'),('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерязева)', 'Донская(Тимерязева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Кудепста', 'Кудепста'), ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),
        ('(А) Блиново(+Вес)', '(А) Блиново(+Вес)'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),
    )

#class flat_search_form(forms.Form):
#    min_ploshad = forms.FloatField(label = 'Мин.площадь', initial='5')
#    max_ploshad = forms.FloatField(label='Макс. площадь', initial='1000')
#    min_prais=forms.IntegerField(label='Цена от:',  initial=0)
#    max_prais = forms.IntegerField(label='Цена до:',  initial=100000000)
#    raion_search = forms.ChoiceField( widget=forms.Select, choices=raion_choises, label='Выберите район',initial='Донская')

class flat_search_form(forms.ModelForm):
    class Meta:
        model = UserProfile1
        fields = ('search_minp','search_maxp','search_minc','search_maxc','search_raion',)


class flat_pict_form(forms.ModelForm):
    class Meta:
        model = flat_obj_gal
        fields = ('npict',)

class seo_pub_form(forms.ModelForm):
    class Meta:
        model = flat_obj
        fields =('nazv',)

########################3
#CLIENTS
##########################

class newclientform(forms.ModelForm):
    class Meta:
        model=clients
        fields=('client_fio','tel','email','category','raion','cel_pokupki','prim','budg_ot','budg_do','ferst_work',
                'prich_otkaza','st_pub')
        widgets = {'raion': SelectMultiple }

class client_edit_form(forms.ModelForm):
    class Meta:
        model=clients
        fields=('raion','cel_pokupki','prim','budg_ot','budg_do','ferst_work',
                'prich_otkaza','st_pub')

        widgets = {'raion': SelectMultiple}


########################
#DOMA
#########################

class doma_new_post(forms.ModelForm):
    class Meta:
        model=flat_obj
        fields=('client_name','client_tel','raion','adress','dom_numb','ploshad','cena_sobstv',
                    'cena_agenstv','prim','h_vid_prava','h_vid_is_okon','h_isp_uch','h_infr','h_etagnost','h_komnat',
                    'h_tip_doma','h_ploshad_uch','h_rast_more',)

    def clean(self):
        cleaned_data = super(doma_new_post, self).clean()
        if len(str(cleaned_data['prim'])) < 300:
            raise ValidationError('меньше 300 символов в описании', code='invalid')
        if str(cleaned_data['raion']) == 'Выбор района':
            raise ValidationError('Не выбран район!', code='invalid')
        return cleaned_data


class doma_edit_form(forms.ModelForm):
     class Meta:
        model = flat_obj
        fields = ('nazv','raion','adress','dom_numb','ploshad','cena_sobstv',
                    'cena_agenstv','prim','h_vid_prava','h_vid_is_okon','h_isp_uch','h_infr','h_etagnost','h_komnat',
                    'h_tip_doma','h_ploshad_uch','h_rast_more',)
     def clean(self):
        cleaned_data = super(doma_edit_form, self).clean()
        if len(str(cleaned_data['prim'])) < 300:
            raise ValidationError('меньше 300 символов в описании', code='invalid')
        if str(cleaned_data['raion']) == 'Выбор района':
            raise ValidationError('Не выбран район!', code='invalid')
        return cleaned_data

##################
#UCHASTKI
#####################

class uc_new_post(forms.ModelForm):
    class Meta:
        model=flat_obj
        fields=('client_name','client_tel','raion','adress','uc_dom_nunb','kadastr','h_infr','vid_razr','relef',
                    'vid_prava','vid_prava','vid','pereferiya','h_ploshad_uch',
                    'cena_sobstv','cena_agenstv','prim',)
    def clean(self):
        cleaned_data = super(uc_new_post, self).clean()
        if len(str(cleaned_data['prim'])) < 300:
            raise ValidationError('меньше 300 символов в описании', code='invalid')
        if str(cleaned_data['raion']) == 'Выбор района':
            raise ValidationError('Не выбран район!', code='invalid')
        #if int(cleaned_data['h_rast_more']) < int(100):
        #    raise ValidationError('Расстояние до моря!', code='invalid')
        if int(cleaned_data['h_ploshad_uch']) == 0:
            raise ValidationError('Площадь участка!', code='invalid')
        return cleaned_data

class uc_edit_form(forms.ModelForm):
    class Meta:
        model=flat_obj
        fields=('raion','adress','kadastr','h_infr','vid_razr','relef',
                    'vid_prava','vid_prava','vid','pereferiya','h_ploshad_uch',
                    'cena_sobstv','cena_agenstv','prim')
        def clean(self):
            cleaned_data = super(uc_new_post, self).clean()
            if len(str(cleaned_data['prim'])) < 300:
                raise ValidationError('меньше 300 символов в описании', code='invalid')
            if str(cleaned_data['raion']) == 'Выбор района':
                raise ValidationError('Не выбран район!', code='invalid')
            #if int(cleaned_data['h_rast_more']) < int(100):
            #    raise ValidationError('Расстояние до моря!', code='invalid')
            if int(cleaned_data['h_ploshad_uch']) == 0:
                raise ValidationError('Площадь участка!', code='invalid')
            return cleaned_data
########
#otchet
#########

class otchet_all_form(forms.ModelForm):
    class Meta:
        model = otchet_nov
        fields = ('nazv_nov','fio_kl','tel_kl','ot_kuda_kl','date_zakr','ploshad','stoimost','komisia','ipoteka',
                  'rasrochka','prim', 'reelt1', 'rielt_proc1', 'reelt2', 'rielt_proc2',
                  'reelt3', 'rielt_proc3', 'reelt4', 'rielt_proc4', 'reelt5', 'rielt_proc5',
                  'reelt6', 'rielt_proc6', 'reelt7', 'rielt_proc7',
                  'reelt8', 'rielt_proc8', 'reelt9', 'rielt_proc9', 'reelt10', 'rielt_proc10',)

    def clean(self):
        cleaned_data = super(otchet_all_form, self).clean()
        proc = int(cleaned_data['rielt_proc1'])+int(cleaned_data['rielt_proc2'])+int(cleaned_data['rielt_proc3'])+int(cleaned_data['rielt_proc4'])\
                +int(cleaned_data['rielt_proc5'])+int(cleaned_data['rielt_proc6'])+int(cleaned_data['rielt_proc7'])+int(cleaned_data['rielt_proc8'])+int(cleaned_data['rielt_proc9'])+int(cleaned_data['rielt_proc10'])
        if int(proc) != 100:
           raise ValidationError('Общая сумма процентов <> 100% и составляет= '+str(proc)+'%', code='invalid')
        if int(cleaned_data['stoimost'])<=int(cleaned_data['komisia']):
                raise ValidationError('Коммисия больше или равна стоимости квартиры' , code='invalid')
        #if cleaned_data['old_date']=='Нет':

        if not timezone.now().date() <= cleaned_data['date_zakr']:
           raise ValidationError('Дата закрытия меньше даты создания сделки', code='invalid')
        return cleaned_data

class otchet_all_form1(forms.ModelForm):#edit for administraciya
    class Meta:
        model = otchet_nov
        fields = ('nazv_nov','fio_kl','tel_kl','ot_kuda_kl','date_sozd','date_zakr','ploshad','stoimost','komisia',
                  'vneseno_komisii','vneseno_komisii_date','vneseno_komisii2','vneseno_komisii_date2',
                  'vneseno_komisii3','vneseno_komisii_date3','vneseno_komisii4','vneseno_komisii_date4',
                  'vneseno_komisii5','vneseno_komisii_date5',
                  'ipoteka','rasrochka','prim', 'reelt1', 'rielt_proc1', 'reelt2', 'rielt_proc2',
                  'reelt3', 'rielt_proc3', 'reelt4', 'rielt_proc4', 'reelt5', 'rielt_proc5', 'reelt6',
                  'rielt_proc6', 'reelt7', 'rielt_proc7',
                  'reelt8', 'rielt_proc8', 'reelt9', 'rielt_proc9', 'reelt10', 'rielt_proc10',)




class all_otchet_filtr_form(forms.Form):
    #fdate = '01.' + str(timezone.datetime.now().month) + '.' + str(timezone.datetime.now().year)
    #st_date = forms.DateField(label='Дата открытия сделки(начало периода)', initial=fdate)
    #end_date = forms.DateField(label='Дата открытия сделки(конец периода)', initial=timezone.datetime.now())

    #layout = Layout(
    #    Row('st_date', 'end_date'),
    #)
    month_choises =(('Январь' , 'Январь'),('Февраль','Февраль'),
    ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'),
    ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'),('Декабрь', 'Декабрь'))
    year_choises = (('2018' , '2018'),('2019','2019'),('2020', '2020'),('2021','2021'))
    year = timezone.datetime.now().year
    moth_ch = timezone.datetime.now().month
    blank_choice = (( year, year),)
    if moth_ch == 1:
        moth_ch = 'Январь'
    if moth_ch == 2:
        moth_ch = 'Февраль'
    if moth_ch == 3:
        moth_ch = 'Март'
    if moth_ch == 4:
        moth_ch = 'Апрель'
    if moth_ch == 5:
        moth_ch = 'Май'
    if moth_ch == 6:
        moth_ch = 'Июнь'
    if moth_ch == 7:
        moth_ch = 'Июль'
    if moth_ch == 8:
        moth_ch = 'Август'
    if moth_ch == 9:
        moth_ch = 'Сентябрь'
    if moth_ch == 10:
        moth_ch = 'Октябрь'
    if moth_ch == 11:
        moth_ch = 'Ноябрь'
    if moth_ch == 12:
        moth_ch = 'Декабрь'
    Mblank_choice = ((moth_ch, moth_ch),)
    month = forms.ChoiceField(choices=Mblank_choice + month_choises, initial=moth_ch, label='Выберите месяц:',)
    year = forms.ChoiceField(choices=blank_choice +  year_choises, initial=year, label='Выберите год:')
    layout = Layout(
        Row('month', 'year'),
    )

###########################
### Domclick Text
###########################
class DmTextForm(forms.ModelForm):
    class Meta:
        model = domclickText
        fields =('text',)

##########################
####  vigruzki
##########################

class vigruzkaForm(forms.ModelForm):
    class Meta:
        fields =('nazv','street','balcons','lift','komnat','prais','etagnost','etag','plosgad','note','pub')
        model = feed

class vigruzkaNovostroikaForm(forms.ModelForm):
    class Meta:
        fields =('nazv','street','balcons','lift','komnat','prais','etagnost','etag','plosgad','note','pub','SaleType')
        model = feed

class vigruzkaGaleryForm(forms.ModelForm):
    class Meta:
        fields = ('npict',)
        model = feed_gallery

class vigGalForm(forms.Form):
    pict = forms.ImageField(label='Фото:')



###########################
### zayavki
##########################
class Urist_new_zayavka_Form(forms.ModelForm):
    class Meta:
        fields = ('fio','tel_kl','kred_manager')
        model = zayavka

class nov_new_zayv_form(forms.ModelForm):
    class Meta:
        fields = ('fio','tel_kl', 'nazv_novostr')
        model = zayavka

class reelt_lich_new_zayv_form(forms.ModelForm):
    class Meta:
        fields = ('fio','tel_kl', 'nazv_novostr','reelt_v_rabote')
        model = zayavka

class all_zayav_form(forms.ModelForm):
    class Meta:
        model = zayavka
        fields =('fio','tel_kl','kanal','raion','komnat','ploshad','budget','prim')

class sriv_zayavka_form(forms.ModelForm):
    class Meta:
        fields = ('komnat','ploshad','odobreno_deneg','pricina_otkaza','prim')
        model = zayavka

#################################
## search forms for reyting
#################################

class search_by_moth_form(forms.Form):
    month_choises =(('Январь' , 'Январь'),('Февраль','Февраль'),
    ('Март', 'Март'), ('Апрель', 'Апрель'), ('Май', 'Май'), ('Июнь', 'Июнь'), ('Июль', 'Июль'),
    ('Август', 'Август'), ('Сентябрь', 'Сентябрь'), ('Октябрь', 'Октябрь'), ('Ноябрь', 'Ноябрь'),('Декабрь', 'Декабрь'))
    year_choises = (('2018' , '2018'),('2019','2019'),('2020', '2020'),('2021','2021'))
    year = timezone.datetime.now().year
    moth_ch = timezone.datetime.now().month
    blank_choice = (( year, year),)
    if moth_ch == 1:
        moth_ch = 'Январь'
    if moth_ch == 2:
        moth_ch = 'Февраль'
    if moth_ch == 3:
        moth_ch = 'Март'
    if moth_ch == 4:
        moth_ch = 'Апрель'
    if moth_ch == 5:
        moth_ch = 'Май'
    if moth_ch == 6:
        moth_ch = 'Июнь'
    if moth_ch == 7:
        moth_ch = 'Июль'
    if moth_ch == 8:
        moth_ch = 'Август'
    if moth_ch == 9:
        moth_ch = 'Сентябрь'
    if moth_ch == 10:
        moth_ch = 'Октябрь'
    if moth_ch == 11:
        moth_ch = 'Ноябрь'
    if moth_ch == 12:
        moth_ch = 'Декабрь'
    Mblank_choice = ((moth_ch, moth_ch),)
    month = forms.ChoiceField(choices=Mblank_choice + month_choises, initial=moth_ch, label='Выберите месяц:',)
    year = forms.ChoiceField(choices=blank_choice +  year_choises, initial=year, label='Выберите год:')

############################################
### for my admin(Vestum & Cian delete)
############################################
class adm_form(forms.Form):
    st_date = forms.DateField(label='Дата открытия сделки(начало периода)')
    end_date = forms.DateField(label='Дата открытия сделки(конец периода)')

    layout = Layout(
        Row('st_date', 'end_date'),
    )

class vestum_count_form(forms.Form):
    vs_count = forms.IntegerField(label='Балы для всех в Вестуме:')


class vestum_poryadok_form(forms.ModelForm):
    class Meta:
        model = vestum_poryadok_feed
        fields = ('poryadok',)