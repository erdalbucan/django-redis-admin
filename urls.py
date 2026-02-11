from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users_list, name="users_list"),
    path("tasks/", views.tasks_list, name="tasks_list"),
]
