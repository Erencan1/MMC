from django.db import models
from .MMC import MMC


@MMC.setdb('DB2')
class Person(models.Model):

    name = models.CharField(max_length=30)