from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.models import Pergunta, PacienteResposta, Triagem
from apps.core.serializers import PerguntasSerializer, PacienteRespostaSerializer, ResponderSerializer, \
    TriagemSerializer, SalvarTriagemSerializer


class PerguntasViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all()
    serializer_class = PerguntasSerializer


class PacienteRespostaViewSet(viewsets.ModelViewSet):
    queryset = PacienteResposta.objects.all()
    serializer_class = PacienteRespostaSerializer

    @action(methods=['POST'], detail=False)
    def responder(self, request):
        serializer = ResponderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(paciente=self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def minhas_respostas(self, request):
        respostas = PacienteResposta.objects.filter(paciente=self.request.user)
        res = []
        for resposta in respostas:
            res.append({
                "id": resposta.pk,
                "id_pergunta": resposta.pergunta.pk,
                "resposta": resposta.resposta
            })

        return Response(res, status=status.HTTP_200_OK)


class TriegaemViewSet(viewsets.ModelViewSet):
    queryset = Triagem.objects.all()
    serializer_class = TriagemSerializer

    @action(methods=['GET'], detail=False)
    def linha_do_tempo(self, request):
        triagens = Triagem.objects.filter(paciente=request.user)
        serializer = TriagemSerializer(triagens, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def store(self, request):
        serializer = SalvarTriagemSerializer(data={'paciente': request.user.id})
        serializer.is_valid(raise_exception=True)
        triegem = serializer.save()
        return Response(TriagemSerializer(instance=triegem).data, status=status.HTTP_201_CREATED)
