from rest_framework import serializers
from .models import Category, Budget, Income, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class MonetaryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'category', 'amount']


class IncomeSerializer(MonetaryTransactionSerializer):
    class Meta(MonetaryTransactionSerializer.Meta):
        model = Income


class ExpenseSerializer(MonetaryTransactionSerializer):
    class Meta(MonetaryTransactionSerializer.Meta):
        model = Expense


class BudgetSerializer(serializers.ModelSerializer):
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ['id', 'name', 'users', 'incomes', 'expenses']
