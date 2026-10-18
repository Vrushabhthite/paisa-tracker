from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.dashboard, name="dashboard"),
    path("add/", v.add, name="add"),
    path("edit/<int:pk>/", v.edit, name="edit"),
    path("delete/<int:pk>/", v.delete, name="delete"),
    path("history/", v.history, name="history"),
    path("export/", v.export, name="export"),
    path("budget/", v.set_budget, name="budget"),
    path("register/", v.register, name="register"),
]
