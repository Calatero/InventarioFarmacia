from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Producto(models.Model):
    nombre = models.CharField(max_length=200,unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0) 

    def __str__(self):
        return self.nombre
         
class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nuevo campo
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades - ${self.precio_total:.2f}"
