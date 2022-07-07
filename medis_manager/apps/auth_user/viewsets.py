from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail

from apps.agravamento.models import Agravamento

from apps.auth_user.models import User, Endereco
from apps.auth_user.serializers import UserSerializer, CreateEnderecoSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = CreateEnderecoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def store(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['POST'], detail=False)
    def clear_add_agravamento(self, request, pk=None):
        paci: User = User.objects.filter(pk=self.request.user.pk).first()

        if len(request.data.get('agravamentos')) == 1:
            if request.data.get('agravamentos')[0] == 11:
                paci.not_agravaments = True
        else:
            paci.not_agravaments = False

        for p in paci.paciente_gravamentos.all():
            agrava = Agravamento.objects.filter(pk=p.pk).first()
            agrava.pacientes.remove(self.request.user)

        for agravamento in request.data.get('agravamentos'):
            agrava = Agravamento.objects.filter(pk=agravamento).first()
            agrava.pacientes.add(self.request.user)

        paci.save()

        return Response('ok', status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def recuperar_senha(self, request, *args, **kwargs):
        resh = 'A7GG33'
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            return Response('Usuário não encontrado', status=status.HTTP_400_BAD_REQUEST)
        user.token = resh
        user.token_created_at = timezone.now()
        user.save()
        send_mail('Solicitação de recuperação de senha',
                  'Olá {}, segue o código para recuperação da senha: {}'.format(user.full_name, resh), None,
                  [request.data['email']])
        return Response('Email enviado', status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def resetar_senha(self, request, *args, **kwargs):
        if User.objects.filter(token=request.data['token']).exists():
            user = User.objects.filter(token=request.data['token']).first()
            if user:
                user.set_password(request.data['password'])
                user.save()
            else:
                return Response('Token inválido.', status=status.HTTP_400_BAD_REQUEST)
            return Response('Senha atualizada', status=status.HTTP_201_CREATED)
        else:
            return Response('Token inválido.', status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, authentication_classes=(), permission_classes=())
    def criar_endereco(self, request):
        serializer = CreateEnderecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok', status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False, authentication_classes=(), permission_classes=())
    def mapa_de_casos(self, request):
        pacientes = User.objects.filter(is_infectado=True)
        lats = []
        for paciente in pacientes:
            if paciente.user_endereco.latitude and paciente.user_endereco.longitude:
                lats.append({
                    "latitude": float(paciente.user_endereco.latitude),
                    "longitude": float(paciente.user_endereco.longitude)
                })
        return Response(lats, status=status.HTTP_200_OK)

