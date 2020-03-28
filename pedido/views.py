from django.shortcuts import render

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models, transaction
from django.db.models import ProtectedError
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from produto.models import Produtos
from .serializers import PedidosSerializer, PedidosCreateSerializer
from .models import Pedidos


# Create your views here.
class PedidoCreateView(CreateAPIView):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosCreateSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data.copy()
        kwargs['context'] = self.serializer_class
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            qtd_solicitada = data['qtd_produtos']
            instance = Produtos.objects.get(id=int(data['nome_produto']))
            nova_qtd_estoque = int(instance.qtd_estoque) - int(qtd_solicitada)

            if int(qtd_solicitada) > int(instance.qtd_estoque):
                return Response(data={'Status': 'Quantidade de produtos no estoque menor do que a solicitação'},
                                status=status.HTTP_400_BAD_REQUEST)

            elif int(qtd_solicitada) == int(instance.qtd_estoque):
                instance.situacao_prod = 0
                instance.qtd_estoque = 0
                instance.save()

                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response(status=status.HTTP_201_CREATED)

            instance.qtd_estoque = nova_qtd_estoque
            serializer.is_valid(raise_exception=True)
            instance.save()
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)


class PedidoListView(ListAPIView):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer
    pagination_class = None


class PedidoDetailUpdateView(RetrieveUpdateAPIView):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer
    serializer_detail_update_class = PedidosSerializer
    pagination_class = None

    def get_pedido(self):
        try:
            clt = Pedidos.objects.get(id=int(self.kwargs['cid']))
        except Pedidos.DoesNotExist:
            clt = None
        return clt

    def get(self, request, *args, **kwargs):
        instance = self.get_pedido()

        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_detail_update_class(instance)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        instance = self.get_pedido()

        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kwargs['context'] = self.serializer_detail_update_class
        serializer = self.serializer_detail_update_class(data=request.data,
                                                         partial=True,
                                                         instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class PedidoDeleteView(DestroyAPIView):
    queryset = Pedidos.objects.all()

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            instance = Pedidos.objects.get(id=int(self.kwargs['cid']))

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            instance.delete()
            instance.delete
        except models.ProtectedError:
            return Response(
                data={'erro': 'Houve algum problema ao deletar esse produto'},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
