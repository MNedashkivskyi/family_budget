from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Budget(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    incomes = models.ManyToManyField('Income', blank=True)
    expenses = models.ManyToManyField('Expense', blank=True)


class MonetaryTransaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

class Income(MonetaryTransaction):
    pass

class Expense(MonetaryTransaction):
    pass