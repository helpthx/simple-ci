from django.db import transaction
from rest_framework import serializers
from django.conf import settings

from produto.models import Produtos
from .models import Pedidos, OPCS_STATUS_PEDIDO


class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'


class PedidosCreateSerializer(serializers.ModelSerializer):
    qtd_produtos = serializers.IntegerField()
    valor_unitario = serializers.CharField(max_length=50)
    data_pedido = serializers.DateField()
    solicitante = serializers.CharField(max_length=50)
    endereco_solicitante = serializers.CharField(max_length=50)
    despachante = serializers.CharField(max_length=50)
    situacao_pedido = serializers.ChoiceField(choices=OPCS_STATUS_PEDIDO)

    class Meta:
        model = Pedidos
        fields = '__all__'

    def validate_valor_unitario(self, valor_unitario):
        if ',' in valor_unitario:
            raise serializers.ValidationError('Insira um preço valido válido')

        return valor_unitario

    @transaction.atomic
    def create(self, validated_data):
        """
        Cria e Retorna uma nova instancia Produtos, given the validated data.
        """
        try:

            pedido = Pedidos.objects.create(**validated_data)
            pedido.save()
        except Exception as e:
            raise e

        return pedido


class PedidosDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        exclude = ('created_at', 'updated_at')

