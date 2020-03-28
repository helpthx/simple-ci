from django.conf.urls import url
from .views import PedidoListView, PedidoCreateView, PedidoDetailUpdateView, PedidoDeleteView

app_name = 'pedido'

urlpatterns = [
    url(r'^list/$', PedidoListView.as_view(), name='pedido_list'),
    url(r'^create/$', PedidoCreateView.as_view(), name='pedido_create'),
    url(r'^detail-update/(?P<cid>\d+)$', PedidoDetailUpdateView.as_view(), name='pedido_put'),
    url(r'^delete/(?P<cid>\d+)$', PedidoDeleteView.as_view(), name='pedido_delete'),
    ]
