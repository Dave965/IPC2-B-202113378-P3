from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="principal"),
    path("enviar_configuracion", views.mensaje_configuracion, name="m_config"),
    path("enviar_consumo", views.mensaje_consumo, name="m_consumo"),
    path("operaciones_sistema", views.menu_operaciones, name="op_sis"),
    path("ayuda", views.ayuda, name="ayuda"),
    path("consultar_datos", views.consultar_datos, name="consulta_datos"),
    path("creacion_datos", views.crear_datos, name="crear_datos"),
    path("creacion_datos/cliente", views.crear_cliente, name="c_cliente"),
    path("creacion_datos/recurso", views.crear_recurso, name="c_recurso"),
    path("creacion_datos/categoria", views.crear_categoria, name="c_categoria"),
    path("creacion_datos/configuracion", views.crear_configuracion, name="c_configuracion"),
    path("creacion_datos/instancia", views.crear_instancia, name="c_instancia"),
    path("creacion_datos/cancelar_instancia", views.cancelar_instancia, name="cancelar_instancia"),
    path("facturacion", views.facturar, name="facturar"),
    path("reportes", views.reportes, name="reportes"),
    path("reportes/factura", views.detalle_factura, name="d_factura"),
    path("reportes/analisis_categoria", views.reporte_analisis_categoria, name="a_categoria"),
    path("reportes/analisis_recurso", views.reporte_analisis_recurso, name="a_recurso"),

]
