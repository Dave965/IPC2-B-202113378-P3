from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="principal"),
    path("enviar_configuracion", views.mensaje_configuracion, name="m_config"),
    path("enviar_consumo", views.mensaje_consumo, name="m_consumo"),
    path("operaciones_sistema", views.menu_operaciones, name="op_sis"),
    path("ayuda", views.ayuda, name="ayuda"),
    path("consultar_datos", views.consultar_datos, name="c_datos"),

]
