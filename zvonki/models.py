from datetime import timezone, datetime
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator
from django.db import models


class zvonok(models.Model):
    auth = models.ForeignKey('auth.User', verbose_name='Риелтор:', on_delete=models.CASCADE, )
    date_sozd = models.DateTimeField(auto_now=False, verbose_name='Дата создания:')
    tel = models.IntegerField('Телефон',help_text='9881112233', blank=False)
    raion_choise = (('Выбор района', 'Выбор района'),('Ахун', 'Ахун'),('Бытха', 'Бытха'),('Виноградная', 'Виноградная'),('Дагомыс', 'Дагомыс'),('Донская', 'Донская'),('Донская(Пасечная)', 'Донская(Пасечная)'),
        ('Донская(Тимерязева)', 'Донская(Тимерязева)'), ('Завокзальный', 'Завокзальный'),('Заречный', 'Заречный'), ('Клубничная', 'Клубничная'),('КСМ', 'КСМ'),
        ('Красная поляна', 'Красная поляна'),('Кудепста', 'Кудепста'), ('Макаренко', 'Макаренко'),('Мамайка', 'Мамайка'),
        ('Мамайский перевал', 'Мамайский перевал'),('Мацеста', 'Мацеста'),('Н.Сочи', 'Н.Сочи'),('Объезная', 'Объезная'),
        ('Пластунская', 'Пластунская'),('Приморье', 'Приморье'), ('Раздольное', 'Раздольное'), ('Светлана', 'Светлана'),('Соболевка', 'Соболевка'),('Транспортная', 'Транспортная'),
        ('Фабрициуса', 'Фабрициуса'), ('Хоста', 'Хоста'), ('Центр', 'Центр'),
        ('(А) Блиново(+Вес)', '(А) Блиново(+Вес)'), ('(А) Гол. дали', '(А) Гол. дали'),
        ('(А) Кур.гор(+Чкал)', '(А) Кур.гор(+Чкал)'), ('(А) Мирный', '(А) Мирный'),
        ('(А) Молдовка', '(А) Молдовка'), ('(А) Центр', '(А) Центр'), ('(А) Чай совхоз', '(А) Чай совхоз'),
    )
    raion=MultiSelectField('Район', choices=raion_choise, max_length=20 , default='Неважно', blank=False)
    subj_choise = (('Неважно','Неважно'),('Студия','Студия'),('Однокомнатная','Однокомнатная'),
                   ('Двухкомнатная','Двухкомнатная'),('Многокомнатная','Многокомнатная'),
                   ('Дом','Дом'),('Участок','Участок'),('Коммерция','Коммерция'))
    subj = models.CharField(verbose_name='Что ищет:', max_length=50, choices=subj_choise, default='Неважно', blank=False)
    cena = models.IntegerField(verbose_name='Бюджет до:', validators=[MinValueValidator(300000)], blank=False, default=800000)
    client_name = models.CharField('Имя клиента:', max_length=45, blank=False)
    prim = models.TextField('Первичная информация:', blank=False)
    coment = models.TextField('Коментарий по проделанной работе', blank=False)
    status_choises = (('Новый','Новый'),('Перезвонить','Перезвонить'),('Недозвонился','Недозвонился'),('В работе','В работе'),
                      ('Архив','Архив'),('В общем доступе','В общем доступе'))
    status_zvonka = models.CharField(max_length=55, verbose_name='Статус звонка', choices =  status_choises, default='Новый')
    prezvonit = models.DateTimeField(verbose_name='Перезвонить: ', blank=False, )#default=datetime.now())

    def __str__(self):
        return self.client_name
    class Meta:
        verbose_name = 'Звонки риелторам'
        verbose_name_plural = 'Звонки риелторам'
