import mptt
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from employees.managers import MyUserManager


class Employee(AbstractBaseUser):
    name = models.CharField(
        _('ФИО'),
        max_length=50,
        unique=True,
        help_text=_(f"Обязательное поле. Длина должна быть не более 50 символов!"),
        error_messages={"unique": _("Указанный пользователь уже есть в базе!")},
    )
    user_name = models.CharField(
        _('Логин'),
        max_length=16,
        unique=True,
        help_text=_("Обязательное поле. Длина должна быть не более 16 символов!"),
        error_messages={"unique": _("Такой логин уже используется!")},
    )
    position = models.CharField(
        _('Должность'),
        max_length=32,
        help_text=_("Обязательное поле. Длина должна быть не более 32 символов!"),
    )
    employment_date = models.DateTimeField(_('Дата приема на работу'))
    monthly_salary = models.IntegerField(_('Заработная плата'), default=0)
    paid_salary = models.IntegerField(_('Всего выплачено'), default=0)
    api_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['name', 'position', 'employment_date']

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
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')


class Relation(MPTTModel):
    name = models.ForeignKey(
        Employee,
        verbose_name=_('Сотрудник'),
        on_delete=models.CASCADE,
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Руководитель'),
    )

    class MPTTMeta:
        level = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        db_table = 'relations'
        verbose_name_plural = _('Отношения')

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
