from rest_framework import generics
from rest_framework.response import Response

from employees.models import Employee, Relation
from employees.serializers import EmployeesListSerializer


class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeesListSerializer
    queryset = Employee.objects.all()


class EmployeeOneLevelListView(generics.ListAPIView):
    serializer_class = EmployeesListSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def get(self, request, *args, **kwargs):
        employees = []
        employee_level = self.kwargs["level"]
        relation_objects = Relation.objects.all()
        for relation_object in relation_objects:
            if relation_object.level == employee_level:
                employees.append(relation_object.name)

        serializer = EmployeesListSerializer(employees, many=True)

        return Response(serializer.data)
