from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from boxApp.forms import EmpleadoForm,EspecialidadForm,AreaForm,ProductoForm,ClienteForm,PedidoForm,PedidoProductoForm
from boxApp.models import Empleado,Area,Especialidad,Producto,Cliente,Pedido,PedidoProducto

# Create your views here.
def inicio(request):
    return render(request,'templatesBoxApp/inicio.html')

#EMPLEADOS
@login_required
def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/empleados/')
    else:
        form = EmpleadoForm()

    return render(request,'templatesBoxApp/empleadoAdd.html',{'form':form})


@login_required
def mostrar_empleados(request):
    empleados = Empleado.objects.all()
    areas = Area.objects.all()
    especialidades = Especialidad.objects.all()

    data = {
        'empleados' : empleados,
        'areas' : areas,
        'especialidades' : especialidades
    }

    return render(request,'templatesBoxApp/empleados.html',data)

@login_required
def cargar_empleado(request,id):
    empleado = get_object_or_404(Empleado,id=id)
    form = EmpleadoForm(instance=empleado)

    return render(request,'templatesBoxApp/empleadoEdit.html',{'form':form, 'empleado':empleado})

@login_required
def modificar_empleado(request,id):
    empleado = get_object_or_404(Empleado,id=id)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST,request.FILES,instance=empleado)
        if form.is_valid():
            if 'foto' in request.FILES:
                empleado.foto = request.FILES['foto']
            form.save()
            return redirect('/empleados/')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request,'templatesBoxApp/empleadoEdit.html',{'form':form, 'empleado':empleado})

@login_required
def eliminar_empleado(request,id):
    empleado = get_object_or_404(Empleado,id=id)

    if request.method == 'POST':
        empleado.delete()
        return redirect('/empleados/')

    return render(request,'templatesBoxApp/eliminarEmpleado.html',{'empleado':empleado})


#ESPECIALIDADES
@login_required
def crear_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/especialidades/')
    else:
        form = EspecialidadForm()

    return render(request,'templatesBoxApp/especialidadAdd.html',{'form':form})

#AREAS
@login_required
def crear_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/areas/')
    else:
        form = AreaForm()

    return render(request,'templatesBoxApp/areaAdd.html',{'form':form})

#PRODUCTOS
@login_required
def mostrar_productos(request):
    productos = Producto.objects.all()

    return render(request,'templatesBoxApp/productos.html',{'productos':productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/productos/')
    else:
        form = ProductoForm()

    return render(request,'templatesBoxApp/productosAdd.html',{'form':form})

@login_required
def cargar_producto(request,id):
    producto = get_object_or_404(Producto,id=id)
    form = ProductoForm(instance=producto)

    return render(request,'templatesBoxApp/productoEdit.html',{'form':form, 'producto':producto})

@login_required
def modificar_producto(request,id):
    producto = get_object_or_404(Producto,id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST,instance=producto)
        if form.is_valid():
            form.save()
            return redirect('/productos/')
    else:
        form = ProductoForm(instance=producto)

    return render(request,'templatesBoxApp/productoEdit.html',{'form':form, 'producto':producto})

@login_required
def eliminar_producto(request,id):
    producto = get_object_or_404(Producto,id=id)

    if request.method == 'POST':
        producto.delete()
        return redirect('/productos/')

    return render(request,'templatesBoxApp/eliminarProducto.html',{'producto':producto})



@login_required
def eliminar_pedido(request,id):
    pedido = get_object_or_404(Pedido,id=id)

    # Check if user can delete this pedido
    if hasattr(request.user, 'is_admin') and request.user.is_admin:
        pass  # Admin can delete any
    elif pedido.cliente == request.user:
        pass  # Client can delete their own
    else:
        return redirect('/pedidos/')  # No permission

    if request.method == 'POST':
        pedido.delete()
        return redirect('/pedidos/')

    return render(request,'templatesBoxApp/eliminarPedido.html',{'pedido':pedido})

#CLIENTES
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.set_password(form.cleaned_data['password'])
            cliente.save()
            return redirect('/clientes/')
    else:
        form = ClienteForm()

    return render(request,'templatesBoxApp/clienteAdd.html',{'form':form})

#PEDIDOS
@login_required
def mostrar_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')

    return render(request,'templatesBoxApp/pedidos.html',{'pedidos':pedidos})

@login_required
@csrf_protect
def crear_pedido(request):
    if request.method == 'POST':
        productos_data = request.POST.getlist('productos')
        cantidades_data = request.POST.getlist('cantidades')

        if productos_data and cantidades_data:
            pedido = Pedido.objects.create()
            total = 0

            for prod_id, cantidad in zip(productos_data, cantidades_data):
                if prod_id and cantidad:
                    producto = get_object_or_404(Producto, id=prod_id)
                    cantidad = int(cantidad)
                    if cantidad > producto.stock:
                        pedido.delete()
                        return render(request,'templatesBoxApp/pedidoAdd.html',{'form':PedidoForm(), 'productos':Producto.objects.all(), 'error': f"No hay suficiente stock para {producto.nombre}"})
                    subtotal = producto.precio * cantidad
                    PedidoProducto.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        subtotal=subtotal
                    )
                    total += subtotal
                    producto.stock -= cantidad
                    producto.save()
            pedido.total = total
            pedido.save()
            return redirect('/pedidos/')

    productos = Producto.objects.all()
    return render(request,'templatesBoxApp/pedidoAdd.html',{'form':PedidoForm(), 'productos':productos})

@login_required
def detalle_pedido(request,id):
    pedido = get_object_or_404(Pedido,id=id)

    return render(request,'templatesBoxApp/pedidoDetail.html',{'pedido':pedido})

def cliente_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'templatesBoxApp/clienteLogin.html', {'error': 'Credenciales inválidas'})
    return render(request, 'templatesBoxApp/clienteLogin.html')
