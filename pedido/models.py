from django.db import models

# Create your models here.
OPCS_STATUS_PEDIDO = [('0', 'Pendente'), ('1', 'Enviado'), ('2' , 'Entregue')]


class Pedidos(models.Model):
    nome_produto = models.ForeignKey(
        'produto.Produtos',
        verbose_name='Produto',
        on_delete=models.CASCADE)

    qtd_produtos = models.IntegerField(verbose_name='Quantidade de produtos pedidos')

    valor_unitario = models.FloatField(max_length=50, verbose_name='Valor por unidade do produto')

    data_pedido = models.DateField()

    solicitante = models.CharField(max_length=100, verbose_name='Nome do solicitante')

    endereco_solicitante = models.CharField(max_length=100, verbose_name='Endereço do solicitante')

    despachante = models.CharField(max_length=100, verbose_name='Nome do despachante')

    situacao_pedido = models.CharField(max_length=10, choices=OPCS_STATUS_PEDIDO, verbose_name='Status do pedido')

    def __str__(self):
        return '%s - %s' % (self.nome_produto, self.nome_produto)