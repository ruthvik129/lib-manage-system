from django.db import models
from datetime import datetime, timedelta



class BooksMaster(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.IntegerField(default=None)


class InventoryMaster(models.Model):
    book = models.ForeignKey(BooksMaster  , related_name='books' , on_delete=models.CASCADE)
    copies_available = models.IntegerField(default=10)

class Issues(models.Model):
    user = models.CharField(max_length=200)
    issued_book = models.ForeignKey(BooksMaster , related_name='book' , on_delete=models.PROTECT , default=None)
    issue_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(default=datetime.now()+timedelta(days=7))
    due_amount = models.IntegerField(default = 0)