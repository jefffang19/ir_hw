from django.urls import path

from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('import_json', views.import_json, name = 'import_json'),
    path('import_xml', views.import_xml, name = 'import_xml'),
    path('show_articles', views.show_articles, name = 'show_articles'),
    # path('search_page', TemplateView.as_view(template_name = 'search_engine/search_page.html') ),
    path('search_page', views.get_keywords, name = 'search_page'),
    path('upload_file', views.upload_file, name = 'upload_file'),
    path('zipf',views.zipf, name = 'zipf'),
    path('import_pubmed', views.import_pubmed, name = 'import_pubmed'),
    path('origin_zipf',views.origin_zipf, name = 'origin_zipf'),
    path('pubmed', views.data_processor_pubmed, name = 'data_processor_pubmed'),
]