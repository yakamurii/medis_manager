from rest_framework import viewsets

from apps.agravamento.models import Agravamento
from apps.agravamento.serializers import AgravamentoSerializer


class AgravamentoViewSet(viewsets.ModelViewSet):
    queryset = Agravamento.objects.all()
    serializer_class = AgravamentoSerializer
