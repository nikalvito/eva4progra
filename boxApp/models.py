from django.db import models
from django.utils import timezone
from boxApp.choices import generos
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os

# Create your models here.
class Especialidad(models.Model):
    nombre = models.CharField(max_length=50,verbose_name='Nombre de la Especialidad')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        db_table = 'especialidad'
        verbose_name ='Especialidad'
        verbose_name_plural = 'Especialidades'

class Area(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=40,verbose_name='Nombre del Área')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"
        
    class Meta:
        db_table = 'area'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'

class Empleado(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name='ID del Empleado')
    nombre = models.CharField(max_length=30,verbose_name='Nombre del Empleado')
    paterno = models.CharField(max_length=30,verbose_name='Apellido Paterno del Empleado')
    materno = models.CharField(max_length=30,verbose_name='Apellido Materno del Empleado',blank=True)
    run = models.CharField(max_length=12,verbose_name='RUN')
    genero = models.CharField(max_length=1,choices=generos,default='o')
    cantHoras = models.PositiveIntegerField(default=20,verbose_name='Cantidad de Horas Trabajadas')
    fechaNac = models.DateField(blank=True,null=True,verbose_name='Fecha de Nacimiento del Empleado')
    especialidad = models.ForeignKey(Especialidad,null=False,on_delete=models.RESTRICT)
    area = models.ForeignKey(Area,null=True,on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def generarNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'empleados'
        fecha = datetime.now().strftime("%d%m%Y_%H%M%S")
        nombre = f"{fecha}.{extension}"
        return os.path.join(ruta,nombre)

    foto = models.ImageField(upload_to=generarNombre,null=True,default='doctores/wntonto.png')



    def __str__(self):
        return f"Emp. {self.nombre} {self.paterno} - {self.especialidad}"

    class Meta:
        db_table = 'empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

class Producto(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name='ID del Producto')
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Producto')
    stock = models.PositiveIntegerField(verbose_name='Cantidad de Stock')
    hora_ingreso = models.DateField(verbose_name='Fecha de Ingreso')
    precio = models.PositiveIntegerField(verbose_name='Precio')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class ClienteManager(BaseUserManager):
    def create_user(self, email, nombre, telefono=None, password=None):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        cliente = self.model(email=email, nombre=nombre, telefono=telefono)
        cliente.set_password(password)
        cliente.save(using=self._db)
        return cliente

    def create_superuser(self, email, nombre, telefono=None, password=None):
        cliente = self.create_user(email, nombre, telefono, password)
        cliente.is_staff = True
        cliente.is_superuser = True
        cliente.save(using=self._db)
        return cliente

class Cliente(AbstractBaseUser):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Cliente')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    password = models.CharField(max_length=128, default='', verbose_name='Contraseña')
    creado = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ClienteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del Pedido')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name='Estado')
    total = models.PositiveIntegerField(default=0, verbose_name='Total')

    def __str__(self):
        return f"Pedido {self.id}"

    def calcular_total(self):
        total = sum(item.subtotal for item in self.pedidoproducto_set.all())
        self.total = total
        self.save()

    class Meta:
        db_table = 'pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, db_column='id_pedido', verbose_name='Pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto', verbose_name='Producto')
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    precio_unitario = models.PositiveIntegerField(verbose_name='Precio Unitario')
    subtotal = models.PositiveIntegerField(verbose_name='Subtotal')

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    class Meta:
        db_table = 'pedidoProducto'
        verbose_name = 'Producto del Pedido'
        verbose_name_plural = 'Productos del Pedido'
