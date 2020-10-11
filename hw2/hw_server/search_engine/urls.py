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
    path('import_pubmed', views.import_pubmed, name = 'import_pubmed'),
    path('zipf',views.zipf, name = 'zipf'), # main hw2 url
    # db api urls
    path('create_stemfreq', views.create_stem_freq, name = 'create_stem_freq'),
    path('create_originfreq', views.create_origin_freq, name = 'create_origin_freq'),
]