from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

from users.models import User
from .forms import SaleForm
from .models import (
    Customer, Category, Product,
    Sale, MonthlyStats, Expense, Purchase, Salary
)

# unregister default Group model
admin.site.unregister(Group)


# ------------------ Translation & Unfold mixin ------------------
class CustomAdminMixin:
    """📌 modeltranslation uchun JS/CSS ulash"""
    class Media:
        js = (
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'all': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


# ------------------ Role-based permission mixin ------------------
class RoleRestrictedAdminMixin(ModelAdmin):
    def has_module_permission(self, request):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.role == User.Role.ADMIN:
            return True
        if user.role == User.Role.MANAGER:
            return self.model in [Salary]
        return False

    def has_view_permission(self, request, obj=None):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.role == User.Role.ADMIN:
            return True
        if user.role == User.Role.MANAGER:
            return self.model in [Salary]
        return False

    def has_add_permission(self, request):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if user.role == User.Role.MANAGER:
            return self.model == Salary
        return False

    def has_change_permission(self, request, obj=None):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_superuser or user.role == User.Role.ADMIN:
            return qs
        if user.role == User.Role.MANAGER:
            if self.model in [Salary]:
                return qs
            return qs.none()
        return qs.none()



# ------------------ Customer admin ------------------
@admin.register(Customer)
class CustomerAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = ("name", "phone_number", "description", "created_at", "created_by")
    search_fields = ("name", "phone_number", "created_by__username")
    ordering = ("-created_at",)


# ------------------ Category admin ------------------
@admin.register(Category)
class CategoryAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = ("title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    list_filter = ("title",)


# ------------------ Product admin ------------------
@admin.register(Product)
class ProductAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = (
        "title", "description", "brand", "price",
        "discount_percentage", "discount_price", "image",
        "amount", "created_at", "updated_at", "category"
    )
    search_fields = ("title", "description", "brand", "category__title")
    ordering = ("-created_at",)


# ------------------ Sale admin ------------------
@admin.register(Sale)
class SaleAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    form = SaleForm
    list_display = ("customer", "product", "description", "quantity", "total_price", "sale_date", "sold_by")
    search_fields = ("product__title", "customer__name", "sold_by__username")
    ordering = ("-sale_date",)


# ------------------ MonthlyStats admin ------------------
@admin.register(MonthlyStats)
class MonthlyStatsAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = ("year", "month", "net_profit", "total_sales", "total_purchases", "total_salaries")
    search_fields = ("year", "month")
    ordering = ("-year", "-month")


# ------------------ Expense admin ------------------
@admin.register(Expense)
class ExpenseAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = ("description", "created_at", "price", "created_by")
    search_fields = ("description", "created_by__username")
    ordering = ("-created_at",)


# ------------------ Purchase admin ------------------
@admin.register(Purchase)
class PurchaseAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = ("product", "quantity", "purchase_price", "total_cost", "purchase_date")
    search_fields = ("product__title",)
    ordering = ("-purchase_date",)


# ------------------ Salary admin ------------------
@admin.register(Salary)
class SalaryAdmin(CustomAdminMixin, RoleRestrictedAdminMixin):
    list_display = ("gave_by", "taken_by", "salary_price", "for_month", "created_at")
    search_fields = ("gave_by__username", "taken_by__username", "salary_price")
    ordering = ("-created_at",)
