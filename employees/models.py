import mptt
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class MyUserManager(BaseUserManager):
    def create_user(self, name, position, employment_date, monthly_salary, api_user, paid_salary=0,  password=None):
        if not name:
            raise ValueError('Пользователь должен иметь имя!')

        user = self.model(
            name=name,
            position=position,
            employment_date=employment_date,
            monthly_salary=monthly_salary,
            paid_salary=paid_salary,
            api_user=api_user,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, position, employment_date, monthly_salary, api_user, paid_salary=0,  password=None):
        user = self.create_user(
            name=name,
            password=password,
            position=position,
            employment_date=employment_date,
            monthly_salary=monthly_salary,
            paid_salary=paid_salary,
            api_user=api_user,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Employee(AbstractBaseUser):
    name = models.CharField('ФИО', max_length=32, unique=True)
    position = models.CharField('Должность', max_length=32)
    employment_date = models.DateTimeField('Дата приема на работу', )
    monthly_salary = models.IntegerField('Заработная плата', default=0)
    paid_salary = models.IntegerField('Всего выплачено', default=0)
    api_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['position', 'employment_date']

    def __str__(self):
        return f'{self.name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Relation(MPTTModel):
    name = models.ForeignKey(Employee,
                             verbose_name='Сотрудник',
                             on_delete=models.CASCADE,
                             )
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            verbose_name='Руководитель',
                            )

    class MPTTMeta:
        level = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        db_table = 'relations'
        verbose_name_plural = 'Отношения'

    def __str__(self):
        return f'{self.name}'

    def validate_max_indent(self):
        max_indent = 5
        lvl = self.parent.level
        if lvl >= max_indent - 1:
            raise ValidationError(f'Максимальная вложенность: {max_indent}')

    def validate_employee_is_equal_lead(self):
        if self.parent.name == self.name:
            raise ValidationError(f'Сотрудник не может подчиняться самому себе!')

    def validate_is_employee_lead(self):
        try:
            Relation.objects.get(name=self.name).name
        except Relation.DoesNotExist:
            pass
        else:
            raise ValidationError(f'У сотрудника может быть только один руководитель!')

    def save(self, *args, **kwargs):
        if self.parent is not None:
            self.validate_max_indent()
            self.validate_employee_is_equal_lead()
        self.validate_is_employee_lead()
        super().save(*args, **kwargs)


mptt.register(Relation, order_insertion_by=['name'])
