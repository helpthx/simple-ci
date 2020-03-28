from django.conf.urls import url

from .views import ProdutoListView, ProdutoCreateView, ProdutoDetailUpdateView, ProdutoDeleteView

app_name = 'produto'

urlpatterns = [
    url(r'^list/$', ProdutoListView.as_view(), name='produto_list'),
    url(r'^create/$', ProdutoCreateView.as_view(), name='produto_create'),
    url(r'^(?P<cid>\d+)/detail-update/$', ProdutoDetailUpdateView.as_view(), name='produto_put'),
    url(r'^(?P<cid>\d+)/delete/$', ProdutoDeleteView.as_view(), name='produto_delete'),
    ]
