from celery.schedules import crontab
from celery.utils.log import get_task_logger
from staff.celery import app

from .models import Employee

logger = get_task_logger(__name__)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour='*/2'), task_pay_salary.s(), name='Pay_every_2_hours')


@app.task
def task_pay_salary():
    employee_objects = Employee.objects.all()
    for employee in employee_objects:
        Employee.objects.filter(name=employee.name).update(paid_salary=employee.monthly_salary + employee.paid_salary)
    logger.info(f"Salary for employees successfully payed!")


@app.task
def async_delete_paid_salary(employees):
    for employee in employees:
        Employee.objects.filter(name=employee).update(paid_salary=0)
        logger.info(f"Paid salary for '{employee}' successfully deleted!")
