from rest_framework import serializers

from apps.auth_user.models import User
from apps.auth_user.serializers import UserSimplesSerializer
from apps.core.models import PacienteResposta, Pergunta, Triagem


class PerguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = ('id', 'titulo', 'descricao', 'about', 'imagem', 'pontos')


class PacienteRespostaSerializer(serializers.ModelSerializer):
    pergunta = PerguntasSerializer()
    paciente = serializers.SerializerMethodField()

    class Meta:
        model = PacienteResposta
        fields = ['id', 'paciente', 'pergunta', 'resposta']

    def get_paciente(self, instance):
        paciente: User = User.objects.filter(pk=instance.paciente.pk).first()
        return {'id': paciente.id, 'nome': paciente.full_name}


class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteResposta
        fields = ['id', 'pergunta', 'resposta']


class TriagemSerializer(serializers.ModelSerializer):
    paciente = UserSimplesSerializer()
    agravamentos_historico = serializers.JSONField(read_only=True)
    respostas_historicio = serializers.JSONField(read_only=True)

    class Meta:
        model = Triagem
        fields = [
            'id',
            'paciente',
            'icon',
            'title',
            'description',
            'total_pontos',
            'datahora_cadastro',
            'agravamentos_historico',
            'respostas_historicio'
        ]


class SalvarTriagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triagem
        fields = ['paciente']
