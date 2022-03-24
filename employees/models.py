import mptt
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Employee(models.Model):
    name = models.CharField("ФИО", max_length=32)
    position = models.CharField("Должность", max_length=32)
    employment_date = models.DateTimeField("Дата приема на работу", )
    monthly_salary = models.IntegerField("Заработная плата", default=0)
    paid_salary = models.IntegerField("Всего выплачено", default=0)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "employees"
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Relation(MPTTModel):
    name = models.ForeignKey(Employee, verbose_name="Сотрудник", on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                            verbose_name="Руководитель")

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        level = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        db_table = "relations"
        verbose_name_plural = "Отношения"


mptt.register(Relation, order_insertion_by=['name'])
