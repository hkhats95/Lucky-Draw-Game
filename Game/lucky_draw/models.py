from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(verbose_name = 'email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username


class LuckyDraw(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    reward = models.CharField(blank=False, null=False, max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    numberofwinners = models.IntegerField(default=3)
    winners = models.ManyToManyField(User, related_name="winnings", blank=True)
    live = models.BooleanField(default=True)
    enddate = models.DateTimeField(auto_now_add=False, blank=False)
    players = models.ManyToManyField(User, related_name='luckydraws', blank=True)

    def __str__(self):
        return self.title


class RaffleTicket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets', blank=False, null=False)
    luckydraw = models.ForeignKey(LuckyDraw, on_delete=models.SET_NULL, null=True, related_name='tickets')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.owner.username}: {self.luckydraw}"



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



