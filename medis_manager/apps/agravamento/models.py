from django.db import models

from apps.auth_user.models import AbstratoModel


class Agravamento(AbstratoModel):
    pacientes = models.ManyToManyField(to='auth_user.User', related_name="paciente_gravamentos", blank=True, default=list)
    titulo = models.CharField(max_length=144)
    descricao = models.TextField()
    fator = models.IntegerField()
    imagem = models.ImageField(upload_to='image_fatores/', verbose_name='Imagem', null=True, blank=True)

    class Meta:
        ordering = ['-datahora_cadastro']

    def __str__(self):
        return self.titulo
