from django.contrib import admin
from django.urls import path, include
from boxApp import views
from django.conf import settings
from django.conf.urls.static import static
from gmApi import views as vistasApi

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.inicio,name='inicio'),
    path('accounts/',include('django.contrib.auth.urls')),

    #EMPLEADOS
    path('empleadoAdd/',views.crear_empleado,name='crearEmpleados'),
    path('empleados/',views.mostrar_empleados,name='empleados'),
    path('empleadoCarga/<str:id>',views.cargar_empleado,name='cargarEmpleado'),
    path('modificarEmpleado/<str:id>',views.modificar_empleado,name='modificarEmpleado'),
    path('eliminarEmpleado/<str:id>',views.eliminar_empleado,name='eliminarEmpleado'),


    #ESPECIALIDADES
    path('especialidadAdd/',views.crear_especialidad,name='crearEspecialidades'),


    #PRODUCTOS
    path('productos/',views.mostrar_productos,name='productos'),
    path('productosAdd/',views.crear_producto,name='crearProductos'),
    path('productoCarga/<str:id>',views.cargar_producto,name='cargarProducto'),
    path('modificarProducto/<str:id>',views.modificar_producto,name='modificarProducto'),
    path('eliminarProducto/<str:id>',views.eliminar_producto,name='eliminarProducto'),


    #AREAS
    path('areaAdd/',views.crear_area,name='crearAreas'),

    #CLIENTES


    #PEDIDOS
    path('pedidos/',views.mostrar_pedidos,name='pedidos'),
    path('pedidoAdd/',views.crear_pedido,name='crearPedido'),
    path('pedido/<str:id>/',views.detalle_pedido,name='detallePedido'),

    #API 
    #path('empleadosApi/',vistasApi.empleadosApi,name='apiEmpleados'),
    #path('productoApi/',vistasApi.productoApi,name='apiProductos'),

    #API RESTFULL
    path('empleadosApi/', vistasApi.empleado_listado, name='apiEmpleado'),
    path('empleadosDetalleApi/<int:pk>/', vistasApi.empleado_detalle, name='empleadoDetalleApi'),
    
    path('productosApi/', vistasApi.producto_listado, name='productoApi'),
    path('productosDetalleApi/<int:pk>/', vistasApi.producto_detalle, name='productoDetalleApi'),

    path('pedidosApi/', vistasApi.pedido_listado, name='pedido_listado'),
    path('pedidosDetallesApi/<int:pk>/', vistasApi.pedido_detalle, name='pedido-detalle'),
    
    # Rutas para PedidoProducto
    path('pedidos_detallesApi/', vistasApi.pedidoproducto_listado, name='pedidoproducto_listado'),
    path('pedidos_detallesApi/<int:pk>/', vistasApi.pedidoproducto_detalle, name='pedidoproducto_detalle'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
