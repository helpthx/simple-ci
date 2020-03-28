from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models, transaction
from django.db.models import ProtectedError
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, DestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .serializers import ProdutosSerializer, ProdutosCreateSerializer
from .models import Produtos


# Create your views here.
class ProdutoCreateView(CreateAPIView):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        kwargs['context'] = self.serializer_class
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class ProdutoListView(ListAPIView):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializer
    pagination_class = None


class ProdutoDetailUpdateView(RetrieveUpdateAPIView):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializer
    serializer_detail_update_class = ProdutosSerializer
    pagination_class = None

    def get_produto(self):
        try:
            clt = Produtos.objects.get(id=int(self.kwargs['cid']))
        except Produtos.DoesNotExist:
            clt = None
        return clt

    def get(self, request, *args, **kwargs):
        instance = self.get_produto()

        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_detail_update_class(instance)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        instance = self.get_produto()

        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kwargs['context'] = self.serializer_detail_update_class
        serializer = self.serializer_detail_update_class(data=request.data,
                                                         partial=True,
                                                         instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'Status': 'Alteração feita com sucesso !!!'}, status=status.HTTP_200_OK)


class ProdutoDeleteView(DestroyAPIView):

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            instance = Produtos.objects.get(id=int(self.kwargs['cid']))

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
