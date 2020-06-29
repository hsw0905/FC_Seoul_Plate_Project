from django.db import models
from django.db.models import F

from restaurant.models import Restaurant
from django.contrib.auth.models import User


class Bookmark(models.Model):
    """
    ForeignKey
    - Restaurant id(PK)
    - User id(PK)
    """
    # , 필요 없음
    # related_name 같은 내용이라 필요 없음
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    # 변수이름 수정 필요, default/null=False 의미가 맞지 않음
    bookmarked_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    # bookmarked_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True,
    #                                     related_name='bookmarked_user', unique=True)

    # convention 맞지 않음
    class Meta:
        ordering = ['-id']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        Restaurant.objects.filter(id=self.restaurant.id).update(rest_count=F('rest_count') + 1)
        # instance = Restaurant.objects.get(id=self.restaurant.id)
        # instance.rest_count += 1
        # instance.save()
        return super().save()

