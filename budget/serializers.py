from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Budget, Income, Expense


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', None),
            password=validated_data['password']
        )
        return user

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
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Budget
        fields = ['id', 'name', 'users', 'incomes', 'expenses']
