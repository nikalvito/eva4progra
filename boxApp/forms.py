from django import forms
from boxApp.choices import generos
from boxApp.models import Especialidad,Area,Empleado,Producto,Cliente,Pedido,PedidoProducto
import datetime


class EmpleadoForm(forms.ModelForm):
    id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'ID del empleado'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Nombre del Doctor'}))
    paterno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Apellido Paterno del Doctor'}))
    materno = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Apellido Materno del Doctor'}),required=False)
    run = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'12.345.678-9'}))
    genero = forms.CharField(widget=forms.Select(choices=generos, attrs={'class':'form-select'}))
    cantHoras = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese la Cantidad de HH Trabajadas por el Doctor'}))
    fechaNac = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'dd/mm/aa','type':'date'}))

    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.all(),
        empty_label="Seleccione una Especialidad",
        widget=forms.Select(attrs={'class':'form-control'})
    )

    area = forms.ModelChoiceField(
        queryset=Area.objects.all(),
        empty_label="Seleccione una Área",
        widget=forms.Select(attrs={'class':'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id'].widget.attrs['readonly'] = True

    class Meta:
        model = Empleado
        fields = '__all__'


    #VALIDACIONES
    def clean_id(self):
        id_value = self.cleaned_data.get('id')
        if self.instance and self.instance.pk:
            # If editing, allow the current ID
            if Empleado.objects.filter(id=id_value).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("El ID del empleado debe ser único")
        else:
            # If creating, check uniqueness
            if Empleado.objects.filter(id=id_value).exists():
                raise forms.ValidationError("El ID del empleado debe ser único")

        try:
            id_value = int(id_value)
        except ValueError:
            raise forms.ValidationError("El ID debe ser un número entero")

        if id_value < 0:
            raise forms.ValidationError("El ID no puede ser negativo")
        return id_value

    def clean_cantHoras(self):
        cantHoras = self.cleaned_data['cantHoras']

        try:
            cantHoras = int(cantHoras)
        except ValueError:
            raise forms.ValidationError("La cantidad de HH debe ser un número entero")

        if cantHoras < 20:
            raise forms.ValidationError("El mínimo de HH que puede trabajar un Doctor son 20")

        if cantHoras > 60:
            raise forms.ValidationError("El máximo de HH que puede trabajar un Doctor son 60")
        return cantHoras

    def clean_fechaNac(self):
        fecha_nac = self.cleaned_data.get('fechaNac')

        minima = datetime.date(1960,1,1)
        maxima = datetime.date.today()

        if fecha_nac:
            if fecha_nac < minima or fecha_nac > maxima:
                raise forms.ValidationError("La fecha de nacimiento debe estar entre 1960 y hoy")
        return fecha_nac

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if nombre and not nombre.isalpha() and ' ' not in nombre:
            raise forms.ValidationError("El nombre debe contener solo letras y espacios")

        return nombre

class ClienteForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Nombre del Cliente'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'cliente@email.com'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'9 1234 5678'}), required=False)

    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        empty_label="Seleccione un Cliente",
        widget=forms.Select(attrs={'class':'form-control'})
    )

    class Meta:
        model = Pedido
        fields = ['cliente']

class PedidoProductoForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        empty_label="Seleccione un Producto",
        widget=forms.Select(attrs={'class':'form-control'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Cantidad'})
    )

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        producto = self.cleaned_data.get('producto')
        if producto and cantidad > producto.stock:
            raise forms.ValidationError(f"No hay suficiente stock. Disponible: {producto.stock}")
        return cantidad

    def clean_paterno(self):
        paterno = self.cleaned_data.get('paterno')

        if paterno and not paterno.isalpha() and ' ' not in paterno:
            raise forms.ValidationError("El apellido paterno debe contener solo letras y espacios")

        return paterno  

    def clean_materno(self):
        materno = self.cleaned_data.get('materno')

        if materno and not materno.isalpha() and ' ' not in materno:
            raise forms.ValidationError("El apellido materno debe contener solo letras y espacios")

        return materno   

class EspecialidadForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Nombre de la Especialidad'}))

    class Meta:
        model = Especialidad
        fields = '__all__'

class AreaForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Nombre del Área'}))
    
    class Meta:
        model = Area
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'ID del producto'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el Nombre del Producto'}))
    stock = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese la cantidad de stock'}))
    hora_ingreso = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'dd/mm/aa','type':'date'}))
    precio = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Precio del producto'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id'].widget.attrs['readonly'] = True

    class Meta:
        model = Producto
        fields = '__all__'

    # VALIDACIONES
    def clean_id(self):
        id_value = self.cleaned_data.get('id')
        if self.instance and self.instance.pk:
            # If editing, allow the current ID
            if Producto.objects.filter(id=id_value).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("El ID del producto debe ser único")
        else:
            # If creating, check uniqueness
            if Producto.objects.filter(id=id_value).exists():
                raise forms.ValidationError("El ID del producto debe ser único")

        try:
            id_value = int(id_value)
        except ValueError:
            raise forms.ValidationError("El ID debe ser un número entero")

        if id_value < 0:
            raise forms.ValidationError("El ID no puede ser negativo")
        return id_value

    def clean_stock(self):
        stock = self.cleaned_data['stock']

        try:
            stock = int(stock)
        except ValueError:
            raise forms.ValidationError("La cantidad de stock debe ser un número entero")

        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo")

        if '.' in str(stock) or ',' in str(stock):
            raise forms.ValidationError("El stock no puede contener decimales")
        return stock

    def clean_hora_ingreso(self):
        hora_ingreso = self.cleaned_data.get('hora_ingreso')

        minima = datetime.date(1960,1,1)
        maxima = datetime.date.today()

        if hora_ingreso:
            if hora_ingreso < minima or hora_ingreso > maxima:
                raise forms.ValidationError("La fecha de ingreso debe estar entre 1960 y hoy")
        return hora_ingreso

    def clean_precio(self):
        precio = self.cleaned_data['precio']

        try:
            precio = int(precio)
        except ValueError:
            raise forms.ValidationError("La cantidad de precio  debe ser un número entero")

        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo")

        if '.' in str(precio) or ',' in str(precio):
            raise forms.ValidationError("El precio no puede contener decimales")
        return precio

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if nombre and not nombre.isalpha() and ' ' not in nombre:
            raise forms.ValidationError("El nombre debe contener solo letras y espacios")

        return nombre
