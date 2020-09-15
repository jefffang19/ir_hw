from django.urls import path

from . import views

urlpatterns = [
    path('import_json', views.import_json, name = 'import_json'),
]