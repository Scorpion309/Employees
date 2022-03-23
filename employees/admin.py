from django.contrib import admin
from .models import Employee, Relations

@admin.register(Employee)
class EployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'monthly_salary', 'paid_salary')
    list_filter = ('position',)

