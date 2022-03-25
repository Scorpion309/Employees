from django.urls import path

from employees.views import EmployeeListView, EmployeeOneLevelListView

urlpatterns = [
    path('all/', EmployeeListView.as_view()),
    path('by_level/<int:level>/', EmployeeOneLevelListView.as_view()),
]
