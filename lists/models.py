from django.db import models
# DONT FORGET TO MAKE THE MIGRATIONS AFTER MODIFYING THIS FILE !!! #############

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
