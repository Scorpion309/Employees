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
    name = models.ForeignKey(Employee,
                             verbose_name="Сотрудник",
                             on_delete=models.CASCADE,
                             )
    parent = TreeForeignKey('self',
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            related_name='children',
                            verbose_name="Руководитель",
                            )

    class MPTTMeta:
        level = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        db_table = "relations"
        verbose_name_plural = "Отношения"

    def __str__(self):
        return f"{self.name}"

    def validate_max_indent(self):
        max_indent = 5
        lvl = self.parent.level
        if lvl >= max_indent - 1:
            raise ValueError(f"Максимальная вложенность: {max_indent}")

    def validate_employee_is_equal_lead(self):
        if self.parent.name == self.name:
            raise ValueError(f"Сотрудник не может подчиняться самому себе!")

    def validate_is_employee_lead(self):
        try:
            Relation.objects.get(name=self.name).name
        except Relation.DoesNotExist:
            pass
        else:
            raise ValueError(f"У сотрудника может быть только один руководитель!")

    def save(self, *args, **kwargs):
        if self.parent is not None:
            self.validate_max_indent()
            self.validate_employee_is_equal_lead()
        self.validate_is_employee_lead()
        super().save(*args, **kwargs)


mptt.register(Relation, order_insertion_by=['name'])
