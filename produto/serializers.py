import locale

from django.db import transaction
from rest_framework import serializers
from django.conf import settings
from .models import Produtos, OPCS_STATUS


class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'


class ProdutosCreateSerializer(serializers.ModelSerializer):
    nome_produto = serializers.CharField(max_length=100)
    valor_unitario = serializers.CharField(max_length=50)
    qtd_estoque = serializers.IntegerField()
    situacao_prod = serializers.ChoiceField(choices=OPCS_STATUS)

    class Meta:
        model = Produtos
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
            produto = Produtos.objects.create(**validated_data)
            produto.save()
        except Exception as e:
            raise e

        return produto


class ProdutosDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        exclude = ('created_at', 'updated_at')

