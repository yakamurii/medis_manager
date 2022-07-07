from rest_framework import serializers

from apps.agravamento.models import Agravamento


class AgravamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agravamento
        fields = ('id', 'titulo', 'descricao', 'fator', 'imagem')
