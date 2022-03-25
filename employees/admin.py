from django.contrib import admin
from django.utils.html import format_html

from .models import Employee, Relation


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'get_lead', 'monthly_salary', 'paid_salary')
    list_filter = ('position', 'relation__level')

    def get_lead(self, obj):
        lead = Relation.objects.get(name=obj).parent
        lead_id = Employee.objects.get(name=lead).id
        return format_html(f'<a href={lead_id}>{lead}</a>')

    get_lead.short_description = u'Руководитель'


@admin.register(Relation)
class RelationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
