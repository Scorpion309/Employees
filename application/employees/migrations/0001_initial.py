# Generated by Django 4.0.3 on 2022-03-29 06:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(error_messages={'unique': 'Указанный пользователь уже есть в базе!'}, help_text='Обязательное поле. Длина должна быть не более 50 символов!', max_length=50, unique=True, verbose_name='ФИО')),
                ('user_name', models.CharField(error_messages={'unique': 'Такой логин уже используется!'}, help_text='Обязательное поле. Длина должна быть не более 16 символов!', max_length=16, unique=True, verbose_name='Логин')),
                ('position', models.CharField(help_text='Обязательное поле. Длина должна быть не более 32 символов!', max_length=32, verbose_name='Должность')),
                ('employment_date', models.DateTimeField(verbose_name='Дата приема на работу')),
                ('monthly_salary', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Заработная плата')),
                ('paid_salary', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Всего выплачено')),
                ('api_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='employees.relation', verbose_name='Руководитель')),
            ],
            options={
                'verbose_name_plural': 'Отношения',
                'db_table': 'relations',
            },
        ),
    ]
