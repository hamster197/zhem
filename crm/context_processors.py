from datetime import timedelta
from crm.models import zayavka, flat_obj
from django.utils import timezone


def main(request):
    n3 = zayavka.objects.filter(status='Свободен').count()
    if not request.user.is_authenticated:
        return {'Ntn3': n3}
    else:
        vestum_count = str(request.user.userprofile1.vestum_count_ads)
        my_ya_obj = flat_obj.objects.filter(author=request.user).count()
        d11 =timezone.datetime.now().date()-timedelta(days=timezone.datetime.now().weekday())
        crm_obj_week_count = flat_obj.objects.filter(author_id=request.user.id, date_sozd__gte=d11).count()
        return {'Ntcrm_obj_week_count':crm_obj_week_count,'Ntn3':n3,'Nt_my_ya_obj':my_ya_obj, 'tvestum_count':vestum_count,}
