from rest_framework import serializers

from apps.agravamento.serializers import AgravamentoSerializer
from apps.auth_user.models import User, Endereco
from apps.core.models import PacienteResposta


class CreateEnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['user', 'rua', 'cep', 'latitude', 'longitude', 'uf', 'cidade', 'bairro']


class UserSimplesSerializer(serializers.ModelSerializer):
    user_endereco = CreateEnderecoSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'full_name', 'user_endereco']


class UserSerializer(serializers.ModelSerializer):
    user_endereco = CreateEnderecoSerializer(many=False, read_only=True)
    paciente_gravamentos = AgravamentoSerializer(many=True, read_only=True)
    respostas = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password',
                  'cpf', 'phone', 'peso', 'altura',
                  'birth_date', 'sexo', 'avatar', 'paciente_gravamentos', 'not_agravaments', 'risco',
                  'respostas', 'total_pontos', 'user_endereco', 'is_infectado']

    def get_respostas(self, instance):
        respostas = []
        paciente_respostas = PacienteResposta.objects.filter(paciente=instance)
        for res in paciente_respostas:
            respostas.append({
                'id': res.pk,
                'pergunta': res.pergunta.descricao,
                'pontos': res.pergunta.pontos,
                'resposta': res.resposta
            })
        return respostas

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
