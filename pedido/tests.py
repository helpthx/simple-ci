from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
from produto.models import Produtos
from pedido.models import Pedidos
from produto.serializers import ProdutosCreateSerializer
from pedido.serializers import PedidosCreateSerializer


class PedidoTeste(APITestCase):

    data = {
        "nome_produto": "Produto 1",
        "valor_unitario": 1200.0,
        "qtd_estoque": 40,
        "situacao_prod": "1"
    }

    data_pedido = {
        "qtd_produtos": 5,
        "valor_unitario": 1200.0,
        "data_pedido": "1200-12-08",
        "solicitante": "Eu",
        "endereco_solicitante": "QNM 09 CONJUNTO C CASA 28",
        "despachante": "Amazon",
        "situacao_pedido": "0",
        "nome_produto": 1}

    def setUp(self):
        self.url_create = reverse('pedido:pedido_create')
        self.url_list = reverse('pedido:pedido_list')

    def teste_create_pedido(self):
        data = self.data.copy()
        data_pedido = self.data_pedido.copy()

        serializer = ProdutosCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        instance = Produtos.objects.create(**data)
        instance.save()

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido['nome_produto'] = int(instance.id)

        serializer = PedidosCreateSerializer(data=data_pedido)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido["valor_unitario"] = '1200,0'

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido["valor_unitario"] = 1200.0
        data_pedido["qtd_produtos"] = 100

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido["nome_produto"] = 0
        data_pedido["situacao_pedido"] = 'TESTE'

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Produtos.objects.count(), 1)

    def teste_list_pedido(self):
        data = self.data.copy()
        data_pedido = self.data_pedido.copy()

        serializer = ProdutosCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        instance = Produtos.objects.create(**data)
        instance.save()

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido['nome_produto'] = int(instance.id)

        serializer = PedidosCreateSerializer(data=data_pedido)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Pedidos.objects.count(), 1)

        response = self.client.get(self.url_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['nome_produto'], int(instance.id))

    def teste_deltail_update_pedido(self):
        data = self.data.copy()
        data_pedido = self.data_pedido.copy()

        serializer = ProdutosCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        instance = Produtos.objects.create(**data)
        instance.save()

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido['nome_produto'] = int(instance.id)

        serializer = PedidosCreateSerializer(data=data_pedido)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Pedidos.objects.count(), 1)

        self.url_detail = reverse('pedido:pedido_put',
                                  kwargs={'cid': str(instance.id)})

        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome_produto'], int(instance.id))

        self.assertEqual(Pedidos.objects.count(), 1)

        data_pedido['solicitante'] = 'teste put'

        response = self.client.put(self.url_detail, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['solicitante'], 'teste put')

        self.assertEqual(Pedidos.objects.count(), 1)

    def teste_delete_pedido(self):
        data = self.data.copy()
        data_pedido = self.data_pedido.copy()

        serializer = ProdutosCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        instance = Produtos.objects.create(**data)
        instance.save()

        self.assertEqual(Produtos.objects.count(), 1)

        data_pedido['nome_produto'] = int(instance.id)

        serializer = PedidosCreateSerializer(data=data_pedido)
        self.assertTrue(serializer.is_valid())

        response = self.client.post(self.url_create, data_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Pedidos.objects.count(), 1)

        self.url_delete = reverse('pedido:pedido_delete',
                                  kwargs={'cid': str(instance.id)})

        response = self.client.get(self.url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertEqual(Pedidos.objects.count(), 1)

        response = self.client.delete(self.url_delete, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Pedidos.objects.count(), 0)
