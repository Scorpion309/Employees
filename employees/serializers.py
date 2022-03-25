from rest_framework import serializers

from employees.models import Employee, Relation


class EmployeesListSerializer(serializers.ModelSerializer):
    lead = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('name', 'position', 'lead', 'monthly_salary', 'paid_salary')

    def get_lead(self, name):
        users = Relation.objects.all()
        for user in users:
            if user.name == name:
                return f'{user.parent}'
