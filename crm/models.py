from datetime import timezone
from django_resized import ResizedImageField

#from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.db import models
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


class news(models.Model):
    nazv=models.CharField('Название', max_length=10)
    text=models.TextField('Текст', max_length=450)
    datep=models.DateField('Дата публикации',blank=True )
    autor=models.ForeignKey( 'auth.User',verbose_name='Автор', on_delete=models.CASCADE)
    #a_tel=.models.ForeignKey('auth.User')
    def __str__(self):
        return self.nazv
    class Meta:
        verbose_name='Новости'
        verbose_name_plural='Новости'


class UserProfile1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField('Телефон',help_text='9881112233',max_length=10, )
    ya_choises = (('Да','Да'),('Нет','Нет'))
    ya =models.CharField('Yandex недвижимость',default='Нет', max_length=3, choices=ya_choises)
    nach_otd = models.CharField('Начальник отдела', default='Нет', max_length=3, choices=ya_choises)
    joomla_usr_id = models.CharField(verbose_name='ID пользователя в Joomla', max_length=10, default='')
    search_minp = models.IntegerField(default=0, verbose_name='Мин.площадь')
    search_maxp = models.IntegerField(default=5000, verbose_name='Макс.площадь')
    search_minc = models.IntegerField(default=0, verbose_name='Мин.цена')
    search_maxc = models.IntegerField(default=100000000, verbose_name='Макс.цена')
    raion_choises = (('Любой', 'Любой'),('Ареда','Ареда'),('Ахун', 'Ахун'),
        ('Барановка село','Барановка село'),('Бытха', 'Бытха'), ('Верхневеселое село','Верхневеселое село'),
        ('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерязева)', 'Донская(Тимерязева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Краевско-Армянское село', 'Краевско-Армянское село'),('Кудепста', 'Кудепста'),
        ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Малая Объездная', 'Малая Объездная'),('Пластунка село', 'Пластунка село'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),
        ('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),('Лазаревское', 'Лазаревское'),
        ('(А) Блиново', '(А) Блиново'), ('(А) Верхнеимеретинская Бухта', '(А) Верхнеимеретинская Бухта'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),('(А) Веселое','(А) Веселое'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),
        ('Орел-Изумруд село','Орел-Изумруд село'),('Черемушки','Черемушки')
                     )
    search_raion = models.CharField(max_length=25, default='Любой', verbose_name='Район', choices=raion_choises)

    vestum_count_ads = models.IntegerField(verbose_name='Кол-во обьявлений в Вестум:', default=0)

    def __unicode__(self):
        return self.user
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        verbose_name_plural='Клиенты'


class flat_obj(models.Model):
    ##################################################################################################
    #       Start of For All
    ##################################################################################################
    nazv = models.CharField(max_length=250, default='', verbose_name='Название обьекта', blank=True)
    allias = models.CharField(max_length=250, default='', verbose_name='Алиас')
    client_name=models.CharField('Имя собственника',max_length=50)
    client_tel = PhoneNumberField('тел собственника', help_text ='+79881234567')
    datep = models.DateField('Дата публикации', blank=True, auto_now=True)
    date_sozd = models.DateField('Дата создания', blank=True, )
    author=models.ForeignKey('auth.User',verbose_name='Автор', on_delete=models.CASCADE)
    status_obj_choises=(('Опубликован','Опубликован'),('Не опубликован','Не опубликован'))
    status_obj=models.CharField('Публикация обьекта',max_length=45, choices=status_obj_choises,default='Опубликован')

    type_choises = (('flat','flat'),('house','house'),('uchastok','uchastok'),('komerc','komerc'))
    type = models.CharField(max_length=25, verbose_name='Тип недвижимости', choices=type_choises, default='flat')
    raion_choise = (('Выбор района', 'Выбор района'),('Ареда','Ареда'),('Ахун', 'Ахун'),
        ('Барановка село','Барановка село'),('Бытха', 'Бытха'), ('Верхневеселое село','Верхневеселое село'),
        ('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерязева)', 'Донская(Тимерязева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Краевско-Армянское село', 'Краевско-Армянское село'),('Кудепста', 'Кудепста'),
        ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Малая Объездная', 'Малая Объездная'),('Пластунка село', 'Пластунка село'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),
        ('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),('Лазаревское', 'Лазаревское'),
        ('(А) Блиново', '(А) Блиново'), ('(А) Верхнеимеретинская Бухта', '(А) Верхнеимеретинская Бухта'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),('(А) Веселое','(А) Веселое'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),
        ('Орел-Изумруд село','Орел-Изумруд село'),('Черемушки','Черемушки')
    )
    raion=models.CharField('Район', choices=raion_choise, max_length=40 , default='Адрес')
    adress = models.CharField(max_length=70, verbose_name='Улица:', help_text='например: Гагарина')
    adress_utf = models.CharField(max_length=270, verbose_name='Улица UTF:', help_text='например: Гагарина', default='')
    dom_numb = models.CharField(max_length=37, verbose_name='Номер дома:', help_text='например: 36 или 11/2 или 16к (Буква обязательно маленкая!)', default='')

    ploshad=models.IntegerField(verbose_name='Площадь(метры)')

    cena_sobstv=models.IntegerField('Цена собственника',validators=[MinValueValidator(300000)])
    cena_agenstv = models.IntegerField('Цена агентства',validators=[MinValueValidator(300000)])
    prim=models.TextField('Описание', blank=True)
    closed = models.BooleanField('Клиент закрыт', default=False)

    text_err = models.BooleanField(verbose_name='Мало текста', default='True')
    pict_err = models.BooleanField(verbose_name='Мало картинок', default='True')
    kv_err = models.BooleanField(verbose_name='Нет № кв', default='True')
    dom_err =models.BooleanField(verbose_name='№ дома', default='True')
    date_vigr_sait = models.DateField(verbose_name='Дата выгрузки на сайт:')#, auto_now=True)

    vs_choise = (('Да','Да'),('Нет','Нет'))
    vestum_pub = models.CharField(verbose_name='Публиковать на Вестум?', max_length=3, default='Нет',choices=vs_choise)

    ##################################################################################################
    #       End of For All
    ##################################################################################################

    ##################################################################################################
    #       Start of Flats
    ##################################################################################################

    kvart_numb = models.CharField(verbose_name='Номер квартиры:', help_text='например: 11', default='',max_length=5, blank=True)

    etap_sdachi_choise=(('Не сдан','Не сдан'),('Рег.УФРС','Рег.УФРС'),('ФЗ-214','ФЗ-214'),('ФЗ-215','ФЗ-215'),('Сдан','Сдан'))
    etap_sdachi=models.CharField('Этап сдачи',max_length=40,choices=etap_sdachi_choise)

    status_gilya_choises=(('Жилое помещение','Жилое помещение'),('Нежилое помещение','Нежилое помещение'),('Часть жил.дома','Часть жил.дома'),('Квартира','Квартира'),('Комната','Комната'))
    status_gilya=models.CharField('Статус жилья',max_length=40,choices=status_gilya_choises)

    klass_gilya_choises=(('Эконом','Эконом'),('Комфорт','Комфорт'),('Бизнес','Бизнес'),('Элит','Элит'))
    klass_gilya=models.CharField('Класс жилья', max_length=45,choices=klass_gilya_choises)

    krdedit_choises=(('Ипотека СберБанк', 'Ипотека СберБанк'), ('Ипотека РоссельхозБанк', 'Ипотека РоссельхозБанк'), ('Ипотека ВТБ24', 'Ипотека ВТБ24'), ('Мат.капитал', 'Мат капитал'), ('Воен ипотека', 'Воен ипотека'),
                     ('Рассрочка', 'Рассрочка'), ('Только наличные', 'Только наличными'))
    kredit=MultiSelectField('Усл.Кредита',  choices=krdedit_choises, default='Ипотека СберБанк')

    remont_choises=(('Черновой','Черновой'),('Чистовой','Чистовой'),('Дизайнерский','Дизайнерский'),('Жилой','Жилой'),('Новый','Новый'))
    remont=models.CharField('Ремонт',max_length=25,choices=remont_choises)

    gaz_choises=(('Нет','Нет'),('Есть','Есть'),('Можно подключить','Можно подключить'),('В процессе подключения','В процессе подключения'))
    gaz=models.CharField('Газ',max_length=40,choices=gaz_choises)

    komn_choises=(('Студия','Студия'),('Однокомнатная','Однокомнатная'),('Двухкомнатная','Двухкомнатная'),
                  ('Трехкомнатная','Трехкомнатная'),('Многокомнатная','Многокомнатная'))
    komnat=models.CharField('Кол-во комнат', max_length=25, choices=komn_choises)


    etag=models.IntegerField('Этаж',default=0)
    etagnost = models.IntegerField('Этажность',default=0)

    vid_is_okon_choises=(('Обычный','Обычный'),('На стену','На стену'),('На море','На море'),('На горы','На горы'))
    vid_is_okon = models.CharField('Вид из окон', max_length=25, choices=vid_is_okon_choises)

    san_usel_choises=(('Совмещенный','Совмещенный'),('Раздельный','Раздельный'))
    san_usel=models.CharField('Санузел', max_length=15,choices=san_usel_choises)

    parking_choises=(('Есть','Есть'),('Нет','Нет'),('Подземный','Подземный'))
    parking=models.CharField('Паркинг',max_length=15,choices=parking_choises)

    ch = (('да','да'),('нет','нет'))
    security = models.CharField(max_length=3, choices=ch, verbose_name='Наличие охраны:', default='нет')
    rubbish_chute = models.CharField(max_length=3, choices=ch, verbose_name='Мусоропровод:', default='нет')
    lift = models.CharField(max_length=3, choices=ch, verbose_name='Лифт:', default='нет')

    bch = (('да','да'),('нет','нет'),('2 балкона','2 балкона'),('2 лоджии','2 лоджии'))
    balcony = models.CharField(max_length=15, choices=bch, verbose_name='Балконы:', default='нет')

    nov_nazv = models.CharField(verbose_name='Название новостройки:',
                                help_text='Для публикации в вестум. Если дому больше 15 лет то напишите Вторичка',
                                max_length=150, default='', blank=True)

    che = (('Нет', 'Нет'),('Да', 'Да') )
    exclusiv = models.CharField(max_length=3, verbose_name='Эксклюзивные права на продажу:', choices=che, default='Нет',)
    kadastr = models.CharField(max_length=30, blank=True, verbose_name='Кадастровый номер', help_text='Необязательно к заполнению', validators=[MinLengthValidator(15)])
    kadastr_pr = models.CharField(max_length=3,default='Нет')
    domclick_choises = (('Да','Да'),('Нет','Нет'))
    appart_pr = models.CharField(verbose_name='Пр.апартаментов', choices=domclick_choises,default='Нет', max_length=3)
    domclick = models.CharField(max_length=3,verbose_name='Yandex', default='Нет',choices=domclick_choises)
    domclick_pub = models.CharField(max_length=3, verbose_name='Опубликовать на Домклик', default='Да',choices=domclick_choises)
    ##################################################################################################
    #       End of Flats
    ##################################################################################################

    ##################################################################################################
    #       Start of Houses
    ##################################################################################################
    h_vid_prava_choises = (('Собственность','Собственность'),('Аренда (49лет)','Аренда (49лет)'),('Размещение эллингов','Размещение эллингов'))
    h_vid_prava = models.CharField(max_length=25,default='n/a',verbose_name='Вид права:', choices=h_vid_prava_choises)

    h_vid_okna_choises = (('На горы и море','На горы и море'),('На горы','На горы'),('На море','На море'),('Обычный','Обычный'))
    h_vid_is_okon =models.CharField(max_length=25,verbose_name='Вид из окон:',choices=h_vid_okna_choises, default='n/a')

    h_isp_uch_choises = (('Поселений (ИЖС)','Поселений (ИЖС)'),('Садовое некоммерческое товарищество','Садовое некоммерческое товарищество')
                         ,('Земля промназначения','Земля промназначения'),('ДНП','ДНП'),('Размещение эллингов','Размещение эллингов'))
    h_isp_uch = models.CharField(max_length=55, verbose_name='Использование участка:',choices=h_isp_uch_choises, default='n/a')

    h_infr_choises =(('Озеленение','Озеленение'),('Детская площадка','Детская площадка'),('Зона отдыха','Зона отдыха'),
                     ('Парковка','Парковка'),('Остановка','Остановка'),('Школа','Школа'),('Больница','Больница'))
    h_infr = models.CharField(max_length=25, verbose_name='Инфраструктура:', choices=h_infr_choises, default='n/a')

    h_etagnost_choises = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'))
    h_etagnost = models.CharField(max_length=3, verbose_name='Этажность:', choices=h_etagnost_choises, default='n/a')

    h_komnat_choises = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'))
    h_komnat = models.CharField(max_length=3, verbose_name='Комнат:', choices=h_komnat_choises, default='n/a')

    h_tip_doma_choises = (('Монолитный','Монолитный'),('Блочный','Блочный'),('Каркасно-монолитный','Каркасно-монолитный'),
                          ('Кирпичный','Кирпичный'),('Деревянный','Деревянный'),('Панельный','Панельный'))
    h_tip_doma = models.CharField(max_length=25, verbose_name='Тип дома', choices= h_tip_doma_choises,default='n/a')

    h_ploshad_uch = models.DecimalField(default='0', decimal_places=1, max_digits=8, verbose_name='Площадь участка (В МЕТРАХ!)')
    h_rast_more = models.IntegerField(verbose_name='Растояние до моря:', default=0)

    ##################################################################################################
    #       End of Houses
    ##################################################################################################

    ##################################################################################################
    #       Start of Uchastki
    ##################################################################################################
    uc_dom_nunb = models.CharField(verbose_name='Номер дома(если есть):', default='',blank=True, max_length=15)
    vid_razr_ch = (('Поселений (ИЖС)','Поселений (ИЖС)'),('Земля промназначения','Земля промназначения'),
                   ('Садовое некоммерческое товарищество','Садовое некоммерческое товарищество'),('ДНП','ДНП')
                   , ('Дачное хозяйство', 'Дачное хозяйство'),('ЛПХ','ЛПХ'))
    vid_razr = models.CharField(verbose_name='Вид разрешеного использования:',max_length=25,default='--',choices=vid_razr_ch)
    relef_ch =(('Ровный','Ровный'),('Уклон','Уклон'))
    relef = models.CharField(verbose_name='Вид рельефа:',max_length=25,default='--',choices=relef_ch)
    vid_prava_ch = (('Собственность','Собственность'),('Аренда (49лет)','Аренда (49лет)'))
    vid_prava = models.CharField(verbose_name='Вид права:',max_length=25,default='--',choices=vid_prava_ch)
    vid_ch = (('На море','На море'),('На горы','На горы'),('На море и горы','На море и горы'))
    vid = models.CharField(verbose_name='Вид',max_length=25, default='--',choices=vid_ch)
    pereferiya_ch = (('Электричество','Электричество'),('Вода','Вода'),('Газ','Газ'),('Канализация','Канализация'))
    pereferiya = MultiSelectField(verbose_name='Коммуникации:',max_length=125,choices=pereferiya_ch,default='--')
    ##################################################################################################
    #       End of For Uchastki
    ##################################################################################################
    def __str__(self):
        return self.komnat
    class Meta:
        verbose_name='Все обьекты'
        verbose_name_plural='Все обьекты'



class flat_obj_gal(models.Model):
    id_gal = models.ForeignKey(flat_obj, related_name='idd_gal', verbose_name='Название', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True, verbose_name='Дата создания')
    npict = ResizedImageField(verbose_name='Фото объекта', upload_to='image/%Y/%m/%d/real', quality=35 )
    class Meta:
        verbose_name = 'Все обьекты галерея'
        verbose_name_plural = 'Все обьекты галерея'
#    def __str__(self):
#        return self.date
#    def delete(self, *args, **kwargs):
        # Note this is a simple example. it only handles delete(),
        # and not replacing images in .save()
#        super(flat_obj_gal, self).delete(*args, **kwargs)
#        self.npict.delete()

class clients(models.Model):
    client_fio=models.CharField(max_length=45,verbose_name='Клиент(ФИО)')
    tel=PhoneNumberField('Телефон клиента(+79881234567)')
    email=models.EmailField('email клиента', default='nomail@nomail.ru')
    raion_choise =  (('Ахун', 'Ахун'),('Адлер', 'Адлер'),('Бытха', 'Бытха'),('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерярева)', 'Донская(Тимерярева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Кудепста', 'Кудепста'), ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),
        ('(А) Блиново(+Вес)', '(А) Блиново(+Вес)'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),

    )
    raion = MultiSelectField('Район:', choices=raion_choise)
    date_sozd=models.DateField('Дата создания:',auto_now=True)
    category_choises=(('Квартиры','Квартиры'),('Дома','Дома'),('Участки','Участки'))
    category=models.CharField('Что ищет',choices=category_choises,max_length=45,default='Квартиры')
    cel_choise=(('ПМЖ','ПМЖ'),('Аренда/Для сдачи','Аренда/Для сдачи'),('Инвестирование','Инвестирование'))
    cel_pokupki=MultiSelectField('Цель покупки',choices=cel_choise)
    prim=models.TextField('Примечание')
    budg_ot=models.IntegerField('Бюджет от:', validators=[MinValueValidator(300000)])
    budg_do=models.IntegerField('Бюджет до:', validators=[MinValueValidator(300000)])
    ferst_work=models.TextField('Проделана первичная работа')
    prich_otkaza=models.TextField('Причина первичного отказа работы')
    auth=models.ForeignKey('auth.User',verbose_name='Автор:', on_delete=models.CASCADE)
    auth_old = models.CharField(max_length=85, default='none' ,verbose_name='Автор(Был раньше):')
    st_choises=(('Только у себя','Только у себя'),('Видно в отделе','Видно в отделе'),('Видно всем','Видно всем'))
    st_pub=MultiSelectField('Oпубликовать в:',default='Только у себя',choices=st_choises)
    closed=models.BooleanField('Клиент закрыт', default=False)
    #otd=models.CharField('Отдел', max_length=45, default=' ')

    def __str__(self):
        return self.client_fio
    class Meta:
        verbose_name='Клиенты'
        verbose_name_plural='Клиенты'
        #auth=models.ForeignKey('auth.User',verbose_name='Автор:')




class uchastok(models.Model):
    author = models.ForeignKey('auth.User', verbose_name='Автор', on_delete=models.CASCADE)
    client_fio=models.CharField(max_length=45,verbose_name='Собственник(ФИО)')
    tel=PhoneNumberField('Телефон собственника(+79881234567)')
    date_sozd=models.DateField('Дата создания:',auto_now=True)
    status_obj_choises=(('Опубликован','Опубликован'),('Не опубликован','Не опубликован'))
    status_obj=models.CharField('Публикация обьекта',max_length=45, choices=status_obj_choises)
    raion_choise =  (('Ахун', 'Ахун'),('Адлер', 'Адлер'),('Бытха', 'Бытха'),('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерярева)', 'Донская(Тимерярева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Кудепста', 'Кудепста'), ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),
        ('(А) Блиново(+Вес)', '(А) Блиново(+Вес)'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),
    )
    raion = models.CharField(verbose_name='Район:',max_length=45, choices=raion_choise)

    adress = models.CharField(max_length=70, verbose_name='Адрес:')
    com_choises=(('На участке','На участке'),('На границе','На границе'),('Нет','Нет'))
    comunications=models.CharField(max_length=25,verbose_name='Комуникации',choices=com_choises)
    gaz_choises=(('Нет','Нет'),('Есть','Есть'),('Можно подключить','Можно подключить'),('В процессе подключения','В процессе подключения'))
    gaz=models.CharField(verbose_name='Газ',choices=gaz_choises,max_length=45)
    nazn_zemli_choises=(('ИЖС','ИЖС'),('СНТ','СНТ'),('ЛПХ','ЛПХ'),('ЖЧ','ЖЧ'))
    nazn_zemli=models.CharField(verbose_name='Назначение земли',max_length=10,choices=nazn_zemli_choises)
    docum_choises = (
    ('Кадастр', 'Кадастр'), ('Тех.паспорт', 'Тех.паспорт'), ('Разр.на строительство', 'Разр.на строительство'),('Свидетельство','Свидетельство'))
    documenti = models.CharField(verbose_name='Документы', max_length=45, choices=docum_choises)
    ploshad = models.IntegerField( verbose_name='Площадь(соток)')
    cena_sobstv = models.IntegerField('Цена собственника', validators=[MinValueValidator(300000)])
    cena_agenstv = models.IntegerField('Цена агенства', validators=[MinValueValidator(300000)])
    prim = models.TextField('Примечание')
    closed = models.BooleanField('Обьект продан', default=False)

    def __str__(self):
        return self.client_fio#,self.cena_sobstv

    class Meta:
        verbose_name = 'Участки'
        verbose_name_plural = 'Участки'


class otchet_nov(models.Model):
    #date_sozd = models.DateField(verbose_name='Дата сделки:', auto_now=True)
    date_sozd = models.DateField(verbose_name='Дата создания сделки:')
    date_zakr = models.DateField(verbose_name='Дата закрытия сделки:')
    nazv_nov = models.CharField(max_length=140, verbose_name='Название объекта:')
    fio_kl = models.CharField(max_length=50, verbose_name='ФИО клиента:')
    tel_kl = PhoneNumberField(verbose_name='тел.Клиента:', help_text='(+79881234567)')

    ot_kuda_choises = (('Другое' , 'Другое'),('Avito','Avito'),('Vestum','Vestum'),('Cian','Cian'),('Сайт компании','Сайт компании'),#('Avito Turbo','Avito Turbo'),
                       ('По рекомендации','По рекомендации'),('Домклик(Сбер)','Домклик(Сбер)'),('Yandex Недвижимость','Yandex Недвижимость'))
    ot_kuda_kl = models.CharField(max_length=20, verbose_name='Канал привлечения клиента:', choices=ot_kuda_choises)

    rielt = models.ForeignKey('auth.User', verbose_name='Риелтор:', on_delete=models.CASCADE)
    rielt_proc = models.IntegerField(verbose_name='Проценты риелтора-инициатора сделки:',default=100, validators=[MaxValueValidator(100)], blank=True)

    ploshad = models.DecimalField(verbose_name='Площадь:', decimal_places=2, max_digits=4,validators=[MinValueValidator(5)], help_text='min 5')
    stoimost = models.IntegerField(verbose_name='Стоимость объекта:', validators=[MinValueValidator(300000)], help_text='min 300 000')
    komisia =  models.IntegerField(verbose_name='Комисия:', validators=[MinValueValidator(1000)], help_text='min 1 000')
    vneseno_komisii = models.IntegerField(verbose_name='Внесенно комисии 1:', default = '0')
    vneseno_komisii_date = models.DateField(verbose_name='Дата внесения комисии 1:', blank=True, null=True)
    vneseno_komisii2 = models.IntegerField(verbose_name='Внесенно комисии 2:', default = 0)
    vneseno_komisii_date2 = models.DateField(verbose_name='Дата внесения комисии 2:', blank=True, null=True)
    vneseno_komisii3 = models.IntegerField(verbose_name='Внесенно комисии: 3', default = 0)
    vneseno_komisii_date3 = models.DateField(verbose_name='Дата внесения комисии 3:', blank=True, null=True)
    vneseno_komisii4 = models.IntegerField(verbose_name='Внесенно комисии 4:', default = 0)
    vneseno_komisii_date4 = models.DateField(verbose_name='Дата внесения комисии 4:', blank=True, null=True)
    vneseno_komisii5 = models.IntegerField(verbose_name='Внесенно комисии 5:', default = 0)
    vneseno_komisii_date5 = models.DateField(verbose_name='Дата внесения комисии 5:', blank=True, null=True)
    ipoteca_choises = (('Да', 'Да'),('Нет', 'Нет'))
    ipoteka = models.CharField(max_length=3,choices=ipoteca_choises,verbose_name='Ипотека:', default='Нет')
    rasr_choises = (('Да', 'Да'), ('Нет', 'Нет'))
    rasrochka = models.CharField(max_length=3,verbose_name='Расрочка:', choices=rasr_choises, default='Нет')
    prim = models.CharField(max_length=1050, verbose_name='Примечание', default=' ', blank=True)

    o_choises = (('',''),('1 Отдел','1 Отдел'),('2 Отдел','2 Отдел'),('3 Отдел','3 Отдел'),('4 Отдел','4 Отдел'),('5 Отдел','5 Отдел'),('6 Отдел','6 Отдел'),('Офис в Адлере','Офис в Адлере'))
    a_choises = [(c.username, c.last_name+ ' '+c.first_name ) for c in User.objects.all().order_by('last_name')]

    reelt1 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №1',blank=True, help_text='Обязательно к заполнению!')
    otd_reelt1 = models.CharField(max_length=25, verbose_name='Отдел:',default='')#,choices=o_choises,default='')
    rielt_proc1 = models.IntegerField(verbose_name='Доля(%) риелтора №1 в сделке:', validators=[MaxValueValidator(100)], default=100, blank=True, help_text='Обязательно к заполнению!')

    reelt2 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №2', blank=True, help_text='Необязательно к заполнению')
    otd_reelt2 = models.CharField(max_length=25, verbose_name='Отдел:',default='',blank=True)#,choices=o_choises,default='')
    rielt_proc2 = models.IntegerField(verbose_name='Доля(%)  риелтора №2 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt3 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №3', blank=True, help_text='Необязательно к заполнению')
    otd_reelt3 = models.CharField(max_length=25, verbose_name='Отдел:',default='', blank=True)#choices=o_choises,default='')
    rielt_proc3 = models.IntegerField(verbose_name='Доля(%) риелтора №3 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt4 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №4', blank=True, help_text='Необязательно к заполнению')
    otd_reelt4 = models.CharField(max_length=25, verbose_name='Отдел:',default='',blank=True)#,choices=o_choises,default='')
    rielt_proc4 = models.IntegerField(verbose_name='Доля(%) риелтора №4 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt5 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №5', blank=True, help_text='Необязательно к заполнению')
    otd_reelt5 = models.CharField(max_length=25, verbose_name='Отдел:',default='',blank=True)#,choices=o_choises,default='')
    rielt_proc5 = models.IntegerField(verbose_name='Доля(%) риелтора №5 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt6 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №6', blank=True, help_text='Необязательно к заполнению')
    otd_reelt6 = models.CharField(max_length=25, verbose_name='Отдел:',default='',blank=True)#,choices=o_choises,default='')
    rielt_proc6 = models.IntegerField(verbose_name='Доля(%) риелтора №6 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt7 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №7', blank=True, help_text='Необязательно к заполнению')
    otd_reelt7 = models.CharField(max_length=25, verbose_name='Отдел:',default='', blank=True)#,choices=o_choises,default='')
    rielt_proc7 = models.IntegerField(verbose_name='Доля(%) риелтора №7 в сделке:', validators=[MaxValueValidator(100)], default=0,help_text='Необязательно к заполнению')

    reelt8 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №8', blank=True, help_text='Необязательно к заполнению')
    otd_reelt8 = models.CharField(max_length=25, verbose_name='Отдел:',default='', blank=True)#,choices=o_choises,default='')
    rielt_proc8 = models.IntegerField(verbose_name='Доля(%) риелтора №8 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt9 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №9', blank=True, help_text='Необязательно к заполнению')
    otd_reelt9 = models.CharField(max_length=25, verbose_name='Отдел:',default='',blank=True)#,choices=o_choises,default='')
    rielt_proc9 = models.IntegerField(verbose_name='Доля(%) риелтора №9 в сделке:', validators=[MaxValueValidator(100)], default=0, help_text='Необязательно к заполнению')

    reelt10 = models.CharField(max_length=100, choices=a_choises, default=' ', verbose_name='Риелтор в сделке №10', blank=True, help_text='Необязательно к заполнению')
    otd_reelt10 = models.CharField(max_length=25, verbose_name='Отдел:',default='', blank=True)#,choices=o_choises,default='')
    rielt_proc10 = models.IntegerField(verbose_name='Доля(%) риелтора №10 в сделке:', default=0, validators=[MaxValueValidator(100)], blank=True, help_text='Необязательно к заполнению')

    all_rielts = models.CharField(max_length=250, default='', verbose_name='все риелторы в сделке:')
    adler_pr = models.CharField(max_length=15,verbose_name='Адлер', blank=True)
    old_date_choises = (('Да', 'Да'), ('Нет', 'Нет'))
    old_date = models.CharField(max_length=3, verbose_name='Сделка проводится задним числом?',default='Нет', choices=old_date_choises)
    sdelka_zakrita_choises = (('Да','Да'),('Нет','Нет'),('Срыв','Срыв'),('Рассрочка','Рассрочка'))
    sdelka_zakrita = models.CharField(max_length=13, choices=sdelka_zakrita_choises, default='Да', verbose_name='Сделка закрыта')
    pr_prosmotra_golovin = models.CharField(max_length=3, verbose_name='Признак просмотра Головиным', default='', blank=True)
    class Meta:
       verbose_name = 'Отчет по сделке'
       verbose_name_plural = 'Отчеты по сделке'
    def __str__(self):
       return self.nazv_nov






class feed(models.Model):
    nazv = models.CharField(max_length=100, verbose_name='Название:', default='')
    date_sozd = models.DateField(auto_now=True, verbose_name='Дата создания')
    author = models.ForeignKey('auth.User',verbose_name='Автор:', on_delete=models.CASCADE)
    street = models.CharField(verbose_name='Улица:',max_length=35)
    komnat = models.IntegerField(verbose_name='Кол-во комнат:', validators=[MinValueValidator(1)], default=1)
    prais = models.IntegerField(verbose_name='Цена:', validators=[MinValueValidator(500000)], help_text='min 500 000')
    etagnost_choise=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
                     ('6', '6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),
                    ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'),
                    ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'))
    etagnost = models.CharField(verbose_name='Этажность', choices=etagnost_choise, max_length=3)
    etag_choise=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),
                     ('6', '6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),
                    ('16', '16'), ('17', '17'), ('18','18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'),
                    ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'))
    etag = models.CharField(verbose_name='Этаж:', choices=etag_choise, max_length=3)
    plosgad = models.IntegerField(verbose_name='Общая площадь:', validators=[MinValueValidator(10)], help_text='min 10')
    note = models.TextField(verbose_name='Описание')
    #date_sozd = models.DateField(verbose_name='Дата создания', auto_now=True)
    balcons_ch=(('Да','Да'),('Нет','Нет'))
    balcons = models.CharField(verbose_name='Балкон',max_length=3, default='Нет',choices=balcons_ch)
    lift_ch = (('Да','Да'),('Нет','Нет'))
    lift = models.CharField(verbose_name='Лифт',max_length=3, default='Нет', choices=lift_ch)
    cat_choses = (('flatSale','Вторичка'),('newBuildingFlatSale','Квартира в новостройке'))
    category = models.CharField(verbose_name='Тип недвижимости',max_length=25,choices=cat_choses, default='flatSale')
    SaleType_choises = (('dupt', 'Договор уступки права требования'), ('dzhsk','Договор ЖСК'), ('free','Свободная продажа'),
                       ('fz214','214-ФЗ'), ('investment','Договор инвестирования'),('pdkp','Предварительный договор купли-продажи'))

    SaleType = models.CharField(max_length=30 ,verbose_name='Тип продажи:', choices=SaleType_choises, default='dupt')
    pub_choises = (('Да','Да'),('Нет','Нет'))
    pub = models.CharField(verbose_name='Публикация:', choices = pub_choises, default = 'Да',max_length=3)
    class Meta:
        verbose_name='Выгрузка'
        verbose_name_plural = 'Выгрузки'
    def __str__(self):
        return self.nazv

class feed_gallery(models.Model):
    id_gal = models.ForeignKey(feed, related_name='idd_gal', verbose_name='Название', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True, verbose_name='Дата создания')
    #author = models.ForeignKey('auth.User',verbose_name='Автор:',default='homka')
    #pict = models.ImageField(verbose_name='Картинка', upload_to='image/%Y/%m/%d')
    npict = ResizedImageField(verbose_name='Фото объекта', upload_to='image/%Y/%m/%d/cian', quality=15)
    class Meta:
        verbose_name = 'Выгрузки галерея'
        verbose_name_plural = 'Выгрузки галерея'
#    def delete(self, *args, **kwargs):
#        # Note this is a simple example. it only handles delete(),
#        # and not replacing images in .save()
#        super(feed, self).delete(*args, **kwargs)
#        self.npict.delete()


class zayavka(models.Model):
    #for all
    fio = models.CharField(max_length=45, verbose_name='ФИО клиента:')
    tel_kl = PhoneNumberField('Тел клиента:',  help_text='+79881234567')
    raion_choise =  (('Неважно','Неважно'),('Ахун', 'Ахун'),('Адлер', 'Адлер'),('Бытха', 'Бытха'),('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерярева)', 'Донская(Тимерярева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Кудепста', 'Кудепста'), ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),
        ('(А) Блиново(+Вес)', '(А) Блиново(+Вес)'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),

    )
    kanal_choises = (('Заявка с сайта','Заявка с сайта'),('Заявка с сайта новостройка','Заявка с сайта новостройка'),
                     ('Заявка с Вестум','Заявка с Вестум'),('Заявка с Avito', 'Заявка с Avito'),('Тел. звонок','Тел. звонок'),('Домклик','Домклик'),('Личный','Личный'))
    kanal = models.CharField(max_length=35, verbose_name='Канал привлечения', default='Тел. звонок',
                              choices=kanal_choises)
    raion = MultiSelectField('Район:', choices=raion_choise, default='Неважно')
    komn_choises = (('Студия','Студия'),('Однокомнатная','Однокомнатная'),('Двухкомнатная','Двухкомнатная'),('Трехкомнатная','Трехкомнатная'),
                    ('Многокомнатная','Многокомнатная'),('Неважно','Неважно'),('Дом','Дом'),('Участок','Участок'),('Коммерция','Коммерция'))
    komnat = models.CharField('Тип недвижимости(что ищет):', max_length=25, choices=komn_choises, default='Неважно')
    ploshad = models.IntegerField(verbose_name='Желаемая площадь:', default=10, validators=[MinValueValidator(10)])
    status_choises = (('Свободен','Свободен'),('Взят в работу','Взят в работу'),('Срыв','Срыв'),('Сделка','Сделка'))
    status = models.CharField(max_length=45, choices=status_choises,verbose_name='Статус заявки',default='Свободен')
    prichina_otkaza_choises = (('Отказ клиента','Отказ клиента'),('Уже купил','Уже купил'),
                      ('Не дозвонились','Не дозвонились'),('Завышенные требования клиента','Завышенные требования клиента'))
    pricina_otkaza = models.CharField(max_length=45, choices=prichina_otkaza_choises ,verbose_name='Причина отказа клиента',default='')
    author=models.CharField(max_length=25 ,verbose_name='Автор:')
    reelt_v_rabote = models.ForeignKey('auth.User', verbose_name='В работе у:', on_delete=models.CASCADE, default='')
    #date_sozd = models.DateField(verbose_name='Дата создания:', auto_now=True)
    date_sozd = models.DateTimeField(verbose_name='Дата создания:', auto_now=True)
    date_zakr = models.DateField(verbose_name='Дата закрытия:')
    date_vzyatia =models.DateTimeField(verbose_name='Взято в работу:', auto_now=True)
    prim = models.TextField(verbose_name='Примечание:')
    #for ipoteca
    kred_manager = models.CharField(max_length=150, verbose_name='Кредитный менеджер:', help_text='ФИО/тел.', default='')
    odobreno_deneg  = models.IntegerField(verbose_name='Одобренно ипотеки:', default=1000000)
    ###########################
    # for all
    ###########################
    budget = models.IntegerField(verbose_name='Бюджет до:', default=1000000, validators=[MinValueValidator(100000)])
    ###########################
    # for novostroiika
    ###########################
    nazv_novostr = models.CharField(max_length=45, verbose_name='Название новостройки', default='')
    class Meta:
        verbose_name = 'Заявки'
        verbose_name_plural = 'Заявки'
    def __str__(self):
         return self.fio


class stat_obj_crm(models.Model):
    date_sozd = models.DateField(verbose_name='Дата создания:', auto_now=True)
    auth_nic = models.CharField(max_length=40, verbose_name='Риелтор login:')
    auth_ful_name = models.CharField(max_length=60, verbose_name='Риелтор ФИО', default='1')
    auth_group = models.CharField(max_length=25, verbose_name='отдел', default='1')
    crm_calc = models.IntegerField(verbose_name='Кол-во обьектов в CRM', default=0)
    crm_calc_kadastr = models.IntegerField(verbose_name='Кол-во обьектов в CRM(без кадастра)', default=0)
    crm_calc_week = models.IntegerField(verbose_name='Кол-во обьектов в CRM(за неделю)', default=0)
    cian_calc = models.IntegerField(verbose_name='Кол-во обьектов в CRM', default=0)

    class Meta:
        verbose_name ='Стат. по обьектам в ЦРМ'
        verbose_name_plural = 'Стат. по обьектам в ЦРМ'
    def __str__(self):
        return self.auth_ful_name


class reyting_po_sdelkam(models.Model):
    auth_nic = models.CharField(max_length=40, verbose_name='Риелтор login:')
    auth_ful_name = models.CharField(max_length=60, verbose_name='Риелтор ФИО', default='1')
    auth_group = models.CharField(max_length=25, verbose_name='отдел', default='1')
    sdelok_calc = models.IntegerField(verbose_name='Кол-во сделок:', default=0)
    sdelok_sum = models.IntegerField(verbose_name='Сумма сделок:', default=0)
    cian_count = models.IntegerField(verbose_name='Объектов в Циан:', default=0)
    crm_count  = models.IntegerField(verbose_name='Объектов в ЦРМ :', default=0)
    class Meta:
        verbose_name = 'Рейтинг по сделкам'
        verbose_name_plural = 'Рейтинг по сделкам'
    def __str__(self):
        return self.auth_ful_name

class reyt_sdelka_otd(models.Model):
    otd = models.CharField(max_length=20,verbose_name='Название отдела',default='')
    kommisia = models.IntegerField(verbose_name='Коммисия',default=0)
    sdelok = models.CharField(max_length=100, verbose_name='Коммисия',default='')
    class Meta:
        verbose_name = 'Рейт по отделам'
        verbose_name_plural = 'Рейт по отделам'
    def __str__(self):
        return self.otd

class cachestvoDomCl(models.Model):
    FIO = models.CharField(max_length=65,verbose_name='ФИО', default='')
    otdel = models.CharField(max_length=45, verbose_name='Отдел',default='')
    vsego = models.IntegerField(verbose_name='Всего обьектов', default='')
    text_err = models.IntegerField(verbose_name='Мало текста',default=0)
    photo_err = models.IntegerField(verbose_name='Мало картинок',default=0)
    kv_numb_err = models.IntegerField(verbose_name='Нет № кв или кадастр',default=0)
    dom_numb_err = models.IntegerField(verbose_name='Нет № кв или кадастр', default=0)

    def __str__(self):
        return self.FIO
    class Meta:
        verbose_name='Качество обьяв'
        verbose_name_plural ='Качество обьявлений'


class domclickText(models.Model):
    dates = models.DateTimeField(auto_now=True,verbose_name='Дата создания:')
    day = models.IntegerField(verbose_name='День публикации в домклик:', default=0)
    text = models.TextField(max_length=1350, verbose_name='Текст для ДомКлик:')
    class Meta:
        verbose_name = 'Тексты для домклик'
        verbose_name_plural = 'Тексты для домклик'
    def __str__(self):
        return self.text




class TmpCianCount(models.Model):
    adler = models.IntegerField(verbose_name='Адлер')
    sochi = models.IntegerField(verbose_name='Сочи')
    class Meta:
        verbose_name = 'Циан'
        verbose_name_plural = 'Циан'

class vestum_poryadok_feed(models.Model):
    choise = (('ПоВозрастанию','ПоВозрастанию'),('ПоУбыванию','ПоУбыванию'))
    date = models.DateField(auto_now=True, verbose_name='Дата изменения')
    poryadok = models.CharField(verbose_name='Порядок выдачи в фиде Vestum', max_length=25,choices=choise)
    class Meta:
        verbose_name = 'Порядок выдачи обьявлений в Циан'
        verbose_name_plural = 'Порядок выдачи обьявлений в Циан'
