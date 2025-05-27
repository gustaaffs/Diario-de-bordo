from django.urls import path
from .views import diario_view, ver_auditoria

urlpatterns = [
    path('diario/', diario_view, name='diario'),
    path('auditoria/', ver_auditoria, name='auditoria'),
]
