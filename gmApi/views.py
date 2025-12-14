from django.shortcuts import render
from boxApp.models import Empleado , Producto, Pedido, PedidoProducto
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from gmApi.serializers import EmpleadoSerializer, ProductoSerializer, PedidoSerializer, PedidoProductoSerializer    


def empleadosApi(request):
    empleados = Empleado.objects.all()
    data = {
        'empleados' : list(
            empleados.values('id','nombre','paterno','materno','run','genero','cantHoras','fechaNac','especialidad','area','creado')
        )
    }
    return JsonResponse(data)

def productoApi(request):
    productos = Producto.objects.all()
    data = {
        'productos' : list(
            productos.values('id','nombre','stock','hora_ingreso','precio','creado')
        )
    }
    return JsonResponse(data)

def pedidoApi(request):
    pedidos = Pedido.objects.all()
    data = {
        'pedido' : list(
            pedidos.values('id','cliente','fecha_pedido','estado','total','creado')
        )
    }
    return JsonResponse(data)

def pedidoProductoApi(request):
    pedido_productos = PedidoProducto.objects.all()
    data = {
        'pedido_productos' : list(
            pedido_productos.values('id','pedido','producto','cantidad','precio_unitario','subtotal','creado')
        )
    }
    return JsonResponse(data)

@api_view(['GET', 'POST'])
def empleado_listado(request):
    if request.method == 'GET':
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def empleado_detalle(request, pk):
    try:
        empleado = Empleado.objects.get(id=pk)
    except Empleado.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EmpleadoSerializer(empleado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        empleado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def producto_listado(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def producto_detalle(request, pk):
    try:
        producto = Producto.objects.get(id=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def pedido_listado(request):
    """
    Lista todos los pedidos o crea un nuevo pedido
    """
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def pedido_detalle(request, pk):
    """
    Obtiene, actualiza o elimina un pedido específico
    """
    try:
        pedido = Pedido.objects.get(id=pk)
    except Pedido.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PedidoSerializer(pedido, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        pedido.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def pedidoproducto_listado(request):
    """
    Lista todos los productos en pedidos o crea una nueva relación pedido-producto
    """
    if request.method == 'GET':
        pedidos_productos = PedidoProducto.objects.all()
        serializer = PedidoProductoSerializer(pedidos_productos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PedidoProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidoproducto_detalle(request, pk):
    """
    Obtiene, actualiza o elimina una relación pedido-producto específica
    """
    try:
        pedido_producto = PedidoProducto.objects.get(id=pk)
    except PedidoProducto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PedidoProductoSerializer(pedido_producto)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PedidoProductoSerializer(pedido_producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        pedido_producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)