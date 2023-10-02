from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='budgets')
    incomes = models.ManyToManyField('Income', blank=True)
    expenses = models.ManyToManyField('Expense', blank=True)

    def __str__(self):
        return self.name


class MonetaryTransaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"

    class Meta:
        abstract = True

class Income(MonetaryTransaction):
    pass

class Expense(MonetaryTransaction):
    pass
