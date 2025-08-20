# main/signals.py
from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from .models import Sale, Purchase, Expense, Salary, MonthlyStats


def update_monthly_stats(year, month):
    """Oylik statistikani yangilash"""
    total_sales = Sale.objects.filter(
        created_at__year=year, created_at__month=month
    ).aggregate(total=Sum('total_price'))['total'] or 0

    total_purchases = Purchase.objects.filter(
        purchase_date__year=year, purchase_date__month=month
    ).aggregate(total=Sum('total_cost'))['total'] or 0

    total_salaries = Salary.objects.filter(
        for_month__year=year, for_month__month=month
    ).aggregate(total=Sum('salary_price'))['total'] or 0

    total_expenses = Expense.objects.filter(
        created_at__year=year, created_at__month=month
    ).aggregate(total=Sum('price'))['total'] or 0

    net_profit = total_sales - (total_purchases + total_salaries + total_expenses)

    stats, created = MonthlyStats.objects.get_or_create(year=year, month=month)
    stats.total_sales = total_sales
    stats.total_purchases = total_purchases
    stats.total_salaries = total_salaries
    stats.net_profit = net_profit
    stats.save()


# -------- SALE --------
@receiver([post_save, post_delete], sender=Sale)
def update_stats_on_sale(sender, instance, **kwargs):
    update_monthly_stats(instance.created_at.year, instance.created_at.month)


# -------- PURCHASE --------
@receiver([post_save, post_delete], sender=Purchase)
def update_stats_on_purchase(sender, instance, **kwargs):
    update_monthly_stats(instance.purchase_date.year, instance.purchase_date.month)


# -------- EXPENSE --------
@receiver([post_save, post_delete], sender=Expense)
def update_stats_on_expense(sender, instance, **kwargs):
    update_monthly_stats(instance.created_at.year, instance.created_at.month)


# -------- SALARY --------
@receiver([post_save, post_delete], sender=Salary)
def update_stats_on_salary(sender, instance, **kwargs):
    update_monthly_stats(instance.for_month.year, instance.for_month.month)
