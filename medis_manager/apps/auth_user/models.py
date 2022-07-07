from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from apps.auth_user.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    MASCULINO = 'MASCULINO'
    FEMININO = 'FEMININO'
    SEXO = (
        (MASCULINO, "Masculino"),
        (FEMININO, "Feminino")
    )
    is_infectado = models.BooleanField(default=False)
    full_name = models.CharField(max_length=144)
    cpf = models.CharField('CPF', max_length=14, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    birth_date = models.DateField()
    phone = models.CharField(max_length=22,blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=SEXO)
    avatar = models.ImageField(upload_to='images', verbose_name='Imagem', null=True, blank=True)
    peso = models.DecimalField(max_digits=3, decimal_places=0, null=True,  blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True,  blank=True)
    token = models.CharField(max_length=22, null=True, blank=True, default=None)
    token_created_at = models.DateField(blank=True, null=True, default=None)
    not_agravaments = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField('staff status', default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def risco(self):
        risco = 'Risco Baixo'
        quantidade_de_riscos = self.paciente_gravamentos.all().count()
        if quantidade_de_riscos == 1:
            if self.paciente_gravamentos.all()[0].descricao == 'Não possuo nenhum critério de agravamento':
                self.not_agravaments = True
                risco = "Nenhum risco"
            else:
                risco = "Risco baixo"
        else:
            if quantidade_de_riscos == 0:
                risco = "Indefinido"
            elif quantidade_de_riscos == 2:
                risco = "Risco médio"
            elif quantidade_de_riscos > 2:
                risco = "Risco alto"

        self.save()
        return risco

    @property
    def total_pontos(self):
        pontos = 0
        for resposta in self.respostas.all():
            if resposta.resposta == True:
                pontos += resposta.pergunta.pontos
        if pontos >= 15:
            self.is_infectado = True
        else:
            self.is_infectado = False
        self.save()
        return pontos

    def __str__(self):
        return '{}'.format(self.full_name)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class AbstratoModel(models.Model):
    datahora_cadastro = models.DateTimeField(auto_now_add=True)
    datahora_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Endereco(AbstratoModel):
    user = models.OneToOneField(User, related_name='user_endereco', on_delete=models.CASCADE)
    rua = models.TextField(null=True, blank=True)
    bairro = models.TextField(null=True, blank=True)
    cep = models.TextField(null=True, blank=True)
    latitude = models.TextField(null=True, blank=True)
    longitude = models.TextField(null=True, blank=True)
    uf = models.TextField(null=True, blank=True)
    cidade = models.TextField(null=True, blank=True)