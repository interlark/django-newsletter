from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .utils import get_avatar_path  # , DEFAULT_AVATAR_PATH


class Profile(models.Model):
    user = models.OneToOneField(User,
                                null=True,
                                on_delete=models.SET_NULL)
    photo = models.ImageField(verbose_name='Аватар',
                              upload_to=get_avatar_path,
                              # default=DEFAULT_AVATAR_PATH,
                              blank=True,
                              null=True,
                              max_length=512)
    gender = models.CharField(verbose_name='Пол',
                              max_length=1,
                              choices=(('M', 'Мужчина'), ('F', 'Женщина')),
                              blank=False,
                              null=False)

    fio_name = models.CharField(verbose_name='ФИО пользователя',
                                max_length=160,
                                blank=False,
                                null=False)

    def __str__(self):
        return self.fio_name

    class Meta:
        ordering = ['id']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(pre_delete, sender=Profile)
def profile_on_pre_delete(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()
