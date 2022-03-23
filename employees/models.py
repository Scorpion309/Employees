import uuid

from django.db import models


# Create your models here.


class Employee(models.Model):
    employee_id = models.UUIDField("employee_id", primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=32)
    position = models.CharField(max_length=32)
    employment_date = models.DateTimeField()
    monthly_salary = models.IntegerField(default=0)
    paid_salary = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Relations(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    level = models.IntegerField()
    lead_id = models.UUIDField()

    def get_level(self):
        return Relations(self.employee_id).level

