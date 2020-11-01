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
    # hw 2
    path('zipf',views.zipf, name = 'zipf'), # main hw2 url
    path('zipf/<int:opt>',views.zipf, name = 'zipf'),
    path('zipf_search', views.zipf_search, name = 'zipf_search'),
    path('zipf_search/<int:subset>', views.zipf_search, name = 'zipf_search'),
    path('show_pk_article/<int:pk>/<slug:keyword>', views.show_pk_article, name ='show_pk_article'),
    path('zipf_ct', views.zipf_ct, name = 'zipf_ct'),
    # db api urls
    path('import_pubmed', views.import_pubmed, name = 'import_pubmed'),
    path('create_stemfreq', views.create_stem_freq, name = 'create_stem_freq'),
    path('create_originfreq', views.create_origin_freq, name = 'create_origin_freq'),
    path('create_revindex', views.create_revindex, name = 'create_revindex'),
    path('search_covid', views.search_covid, name = 'search_covid'),
    # hw3
    path('create_model', views.create_model, name = 'create_model'),
]