from celery.utils.log import get_task_logger
from staff.celery import app

from .models import Employee

logger = get_task_logger(__name__)


# @app.task
# def task_pay_salary():
#     logger.info(f"Salary paid!")

@app.task
def async_delete_paid_salary(employees):
    for employee in employees:
        Employee.objects.filter(name=employee).update(paid_salary=0)
        logger.info(f"Paid salary for '{employee}' successfully deleted!")
