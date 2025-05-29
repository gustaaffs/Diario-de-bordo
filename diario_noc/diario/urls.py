from django.urls import path, include
from .views import diario_view, ver_auditoria

urlpatterns = [
    path('diario/', diario_view, name='diario'),
    path('diario/auditoria/', ver_auditoria, name='auditoria'),
    path('diario/accounts/', include('django.contrib.auth.urls')),
]
