from django.urls import path

from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('import_json', views.import_json, name = 'import_json'),
    path('show_articles', views.show_articles, name = 'show_articles'),
    path('search_page', TemplateView.as_view(template_name = 'search_engine/search_page.html') ),
]