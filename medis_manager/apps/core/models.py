from django.db import models
import jsonfield

from apps.auth_user.models import AbstratoModel
from apps.notifications.models import Notifications


class Pergunta(AbstratoModel):
    titulo = models.CharField(max_length=144)
    descricao = models.TextField(null=True, blank=True)
    about = models.TextField(default='')
    imagem = models.ImageField(upload_to='image_perguntas/', verbose_name='Imagem', null=True, blank=True)
    pontos = models.IntegerField()

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.titulo


class PacienteResposta(AbstratoModel):
    paciente = models.ForeignKey(to='auth_user.User', related_name='respostas', on_delete=models.CASCADE)
    pergunta = models.ForeignKey(to='Pergunta', related_name='respostas', on_delete=models.CASCADE)
    resposta = models.BooleanField(default=False)

    class Meta:
        db_table = "agravamento_paciente_agravamento"
        unique_together = ('paciente', 'pergunta')

    def save(self, *args, **kwargs):
        respondeu = PacienteResposta.objects.filter(paciente=self.paciente, pergunta=self.pergunta).first()
        if respondeu:
            pass
            # raise serializers.ValidationError('O paciente já respondeu essa pergunta')
        return super(PacienteResposta, self).save(*args, **kwargs)


class Triagem(AbstratoModel):
    paciente = models.ForeignKey(to='auth_user.User', related_name='triagens', on_delete=models.CASCADE)
    title = models.TextField()
    icon = models.CharField(max_length=80, default="", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_pontos = models.IntegerField()
    agravamentos_historico = jsonfield.JSONField(default=list)
    respostas_historicio = jsonfield.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.total_pontos = self.paciente.total_pontos

        respostas_history = []
        agravaments_history = []

        for a in self.paciente.respostas.all():
            data = {
                'pergunta': {
                    'id': a.id,
                    'titulo': a.pergunta.titulo,
                    'pontos': a.pergunta.pontos,
                },
                'resposta': a.resposta
            }
            respostas_history.append(data)

        for agrav in self.paciente.paciente_gravamentos.all():
            data = {
                'agravamento': {
                    'id': agrav.id,
                    'descricao': agrav.descricao
                }
            }
            agravaments_history.append(data)

        self.agravamentos_historico = agravaments_history
        self.respostas_historicio = respostas_history

        if self.total_pontos == 0:
            self.title = "Nenhuma probabilidade de infecção."
            self.icon = '/media/timeLine/success.png'
            self.description = "Você não se enquadra como suspeito."
        elif self.total_pontos > 0 and self.total_pontos <= 6:
            self.title = "Baixa probabilidade de infecção."
            self.icon = '/media/timeLine/baixo.png'
            self.description = "Recomendamos buscar a unidade básica de saúde. Se estiver sem médico/enfermeiro ou estiver fora do horário, buscar o centro municipal de referência para covid."
        elif self.total_pontos >= 7 and self.total_pontos <= 14:
            self.title = "Média probabilidade de infecção."
            self.icon = '/media/timeLine/suspeito.png'
            self.description = "Recomendamos buscar diretamente o centro de referência covid. Em caso de dificuldades de transporte ou deslocamento ir a unidade básica mais próxima de casa ou UPA mais próxima."
        elif self.total_pontos >= 15:
            self.title = "Alta probabilidade de infecção."
            self.icon = '/media/timeLine/infectado.png'
            self.description = "Recomendamos ir diretamente para UPA ou acionar o Samu (192)"

        Notifications.objects.create(user_id=self.paciente.id, title=self.title,
                                     message=self.description)
        return super(Triagem, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-datahora_cadastro']

    def __str__(self):
        return self.paciente.full_name
