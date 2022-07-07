from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.notifications.models import Notifications
from apps.notifications.serializers import NotificationSerializer


class NotificationViewset(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notifications.objects.all()

    @action(methods=['GET'], detail=False)
    def minhas_notificacoes(self, request):
        notificacoes = Notifications.objects.filter(user=self.request.user).all().order_by('lida')
        serializer = NotificationSerializer(notificacoes, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def ler_notificacao(self, request):
        notificacoes = Notifications.objects.filter(user=self.request.user).all()
        for notifica in notificacoes:
            notifica.lida = True
            notifica.save()
        return Response("ok", status=status.HTTP_200_OK)
