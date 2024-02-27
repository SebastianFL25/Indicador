#path
from django.urls import path

# view
from unit.api.views import create_unit,UnitListView

urlpatterns = [
    path('obtent/', create_unit, name='unit-obtent'),
    path('list/',UnitListView.as_view(),name='unit-list-month-range'),
    ]