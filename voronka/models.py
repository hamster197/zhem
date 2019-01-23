from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class status_klienta(models.Model):
    status_id = models.DecimalField(verbose_name='Статус заявки:(№ пп)', max_digits=5, decimal_places=2,null=True)
    status_nazv = models.CharField(verbose_name='Статус заявки:(Название)', max_length=40, default='')
    voronka_counts = models.IntegerField(verbose_name='Кол для воронки продаж', default=0)
    def __str__(self):
        return self.status_nazv
    class Meta:
        verbose_name = 'Статус сделки(Справочник)'
        verbose_name_plural = 'Статус сделки(Справочник)'
        ordering =['status_id']

class status_klienta_all(models.Model):
    zayavka_vr_id = models.ForeignKey('zayavka_vr', on_delete=models.CASCADE, null=True,
                                      related_name='idd_st', verbose_name='Статус заявки:')
    date_sozd = models.DateField(verbose_name='Дата:', null=True, blank=True,)
    status = models.ForeignKey('status_klienta', on_delete=models.CASCADE, null=True, verbose_name='Статус заявки:')
    auth = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, verbose_name='Автор:')
    otdel = models.CharField(max_length=45, verbose_name='Отдел')
    def __str__(self):
        return self.otdel
    class Meta:
        verbose_name = 'Статус сделки(Даты)'
        verbose_name_plural = 'Статус сделки(Даты)'
        ordering = ['-pk']

class kanal_pr1(models.Model):
    kanal = models.CharField(max_length=45, verbose_name='Канал привлечения:')
    voronka_counts = models.IntegerField(verbose_name='Кол для воронки продаж', default=0)
    def __str__(self):
        return self.kanal
    class Meta:
        verbose_name = 'Канал привлечения'
        verbose_name_plural = 'Канал привлечения'

class zayavka_subj(models.Model):
    subj = models.CharField(verbose_name='Что ищет:', max_length=55)
    def __str__(self):
        return self.subj
    class Meta:
        verbose_name = 'Тип надвижимости(Справочник)'
        verbose_name_plural = 'Тип надвижимости(Справочник)'

class zayavka_vr(models.Model):
    date_sozd = models.DateField(verbose_name='Дата создания(Входящая заявка):', null=True, blank=True)
    date_vzatia = models.DateField(verbose_name='Дата взятия в работу(Входящая заявка):', null=True, blank=True)
    date_zakr = models.DateField(verbose_name='Дата закрытия(Входящая заявка):', null=True, blank=True)
    a_choises = [(c.id, c.last_name + ' ' + c.first_name) for c in
                 User.objects.filter(is_active=True).order_by('last_name')]
    rielt = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, verbose_name='Автор:')
    kanal = models.ForeignKey(kanal_pr1,  on_delete=models.CASCADE, null=True, verbose_name='Канал привлечения:')
    estate = models.ForeignKey(zayavka_subj, on_delete=models.CASCADE, null=True, verbose_name='Что ищет:')
    otdel = models.CharField(max_length=55, verbose_name='Oтдел', default='')
    tek_status = models.CharField(max_length=55, verbose_name='Текущий статус', null=True)
    tek_status_date = models.DateField(verbose_name='Текущий статус(Дата)', null=True)
    budget = models.IntegerField(verbose_name='Бюджет:', default=0,validators=[MinValueValidator(300000)])
    stat_zayv_spr = models.ManyToManyField(status_klienta_all, related_name='status_zayv_spr', blank=True)
    fio = models.CharField(max_length=85, verbose_name='ФИО Клиента', default='', blank=False, null=False)
    tel = PhoneNumberField('Тел. собственника', help_text ='+79881234567', default='', blank=False, null=False)
    tel_dop = PhoneNumberField('Доп. тел собственника(если есть)', help_text='+79881234567', default='', blank=True, null=True)
    email = models.EmailField(verbose_name='email(если есть)', blank=True, help_text='email@mail.ru')
    def __str__(self):
        return str(self.estate)+' '+str(self.budget)+'rub. '+str(self.rielt)
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявка'
        ordering = ['-date_sozd','-pk']

class comment(models.Model):
    komm_id = models.ForeignKey(zayavka_vr, related_name='kom_id', on_delete=models.CASCADE, null=True,)
    date_sozd = models.DateTimeField(verbose_name='Дата создания:', auto_now=True)
    comment = models.TextField(verbose_name='Комментарий')
    def __str__(self):
        return str(self.date_sozd)
    class Meta:
        verbose_name_plural = 'Комментарий'
        verbose_name = 'Комментарий'
        ordering = ['-date_sozd']

class zadachi_spr(models.Model):
    zadacha = models.CharField(max_length=55, verbose_name='Задача:', )
    def __str__(self):
        return self.zadacha
    class Meta:
        verbose_name = 'Задачи(Справочник)'
        verbose_name_plural = 'Задачи(Справочник)'

class zadachi(models.Model):
    zadacha_idd = models.ForeignKey(zayavka_vr, related_name='zadacha_id', on_delete=models.CASCADE)
    zadacha_date = models.DateField(verbose_name='Дата:')
    zadacha_time = models.TimeField(verbose_name='Время:')
    zadacha = models.ForeignKey(zadachi_spr, verbose_name='Задача:', related_name='zadacha_id', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.zadacha)
    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'
        ordering = ['-zadacha_date']
