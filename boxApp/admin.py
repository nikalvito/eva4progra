from django.contrib import admin

# Register your models here.
from boxApp.models import Especialidad, Area, Empleado, Cliente

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']

class AreaAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre']

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre','paterno','materno','run','genero','cantHoras','fechaNac','especialidad','area']


admin.site.register(Especialidad,EspecialidadAdmin)
admin.site.register(Area,AreaAdmin)
admin.site.register(Empleado,EmpleadoAdmin)
