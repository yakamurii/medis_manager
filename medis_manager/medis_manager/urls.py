from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings

from apps.agravamento.viewsets import AgravamentoViewSet
from apps.auth_user.viewsets import UserViewSet, EnderecoViewSet
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static

from apps.core.viewsets import PerguntasViewSet, PacienteRespostaViewSet, TriegaemViewSet
from apps.notifications.viewsets import NotificationViewset

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'agravametos', AgravamentoViewSet)
router.register(r'perguntas', PerguntasViewSet)
router.register(r'respostas', PacienteRespostaViewSet)
router.register(r'notifications', NotificationViewset)
router.register(r'triagem', TriegaemViewSet)
router.register(r'endereco', EnderecoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)