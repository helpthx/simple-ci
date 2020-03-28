from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
from produto.models import Produtos
from produto.serializers import ProdutosCreateSerializer


class ProdutoTeste(APITestCase):

    data = {
        "nome_produto": "Produto 1",
        "valor_unitario": 1200.0,
        "qtd_estoque": 0,
        "situacao_prod": "0"
    }

    def setUp(self):
        self.url_create = reverse('produto:produto_create')
        self.url_list = reverse('produto:produto_list')

    def teste_create_produto(self):
        data = self.data.copy()
        serializer = ProdutosCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(self.url_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Produtos.objects.count(), 1)

        data["valor_unitario"] = 1200.0

        response = self.client.post(self.url_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Produtos.objects.count(), 1)

        data["valor_unitario"] = 1200.0
        data["situacao_prod"] = 80

        response = self.client.post(self.url_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Produtos.objects.count(), 1)

        data["situacao_prod"] = 0
        data["qtd_estoque"] = 'TESTE'

        response = self.client.post(self.url_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Produtos.objects.count(), 1)

    def teste_list_produto(self):
        data_list = self.data.copy()
        serializer = ProdutosCreateSerializer(data=data_list)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(self.url_create, data_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Produtos.objects.count(), 1)

        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nome_produto'], data_list['nome_produto'])

    def teste_deltail_update_produto(self):
        data_list = self.data.copy()
        serializer = ProdutosCreateSerializer(data=data_list)
        self.assertTrue(serializer.is_valid())

        instance = Produtos.objects.create(**data_list)
        instance.save()

        self.assertEqual(Produtos.objects.count(), 1)

        self.url_detail = reverse('produto:produto_put',
                                  kwargs={'cid': instance.id})

        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome_produto'], data_list['nome_produto'])

        self.assertEqual(Produtos.objects.count(), 1)

        data_list['nome_produto'] = 'teste put'
        response = self.client.put(self.url_detail, data_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'Status': 'Alteração feita com sucesso !!!'})

    def teste_delete_produto(self):
        data_list = self.data.copy()
        serializer = ProdutosCreateSerializer(data=data_list)
        self.assertTrue(serializer.is_valid())

        instance = Produtos.objects.create(**data_list)
        instance.save()

        self.assertEqual(Produtos.objects.count(), 1)

        self.url_delete = reverse('produto:produto_delete',
                                  kwargs={'cid': instance.id})

        response = self.client.get(self.url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertEqual(Produtos.objects.count(), 1)

        response = self.client.delete(self.url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Produtos.objects.count(), 0)
