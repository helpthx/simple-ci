from django.db import models


# Create your models here.
OPCS_STATUS = [('0', 'Indisponivel'), ('1', 'Disponivel')]


class Produtos(models.Model):
    nome_produto = models.CharField(max_length=100, verbose_name='Nome do produto')

    valor_unitario = models.FloatField(max_length=50, verbose_name='Valor unitário')

    qtd_estoque = models.IntegerField(verbose_name='Quantidade no estoque')

    situacao_prod = models.CharField(max_length=50, choices=OPCS_STATUS, verbose_name='Status do produto')

    def __str__(self):
        return '%s - %s' % (self.nome_produto, self.nome_produto)

    def delete(self, using=None, keep_parents=False):
        nome_produto = self.nome_produto
        super(Produtos, self).delete(using, keep_parents)
