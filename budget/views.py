from rest_framework import filters, viewsets
from django_filters import rest_framework as django_filters
from .models import Category, Budget, Income, Expense
from .serializers import CategorySerializer, BudgetSerializer, IncomeSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_fields = ('category',)


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_fields = ('category',)