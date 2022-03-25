from django.contrib import admin
from django.utils.html import format_html

from .models import Employee, Relation


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'get_lead', 'monthly_salary', 'paid_salary')
    list_filter = ('position',)

    def get_lead(self, obj):
        lead = Relation.objects.get(name=obj).parent
        lead_id = Employee.objects.get(name=lead).id
        return format_html(f"<a href={lead_id}>{lead}</a>")

    get_lead.short_description = u'Руководитель'

    def get_level(self, obj):
        return Relation.objects.get(name=obj).level

    get_level.short_description = u'Уровень иерархии'


@admin.register(Relation)
class RelationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
