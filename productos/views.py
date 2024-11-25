from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Producto, Venta
from django.contrib import messages
from .forms import VentaForm
from .forms import ProductoForm
from .models import Producto
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('productos:lista_productos')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'productos/login.html', {'form': form})

# Vista de Logout
def logout_view(request):
    logout(request)
    return redirect('productos:login')

# Vista de Lista de Productos (solo accesible para usuarios autenticados)
@login_required
def lista_productos(request):
    query = request.GET.get('q', '')

    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()

    return render(request, 'productos/lista_productos.html', {'productos': productos})

# Vista de inventario
def inventario_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo producto en la base de datos
            form.save()
            return redirect('productos:inventario')  # Redirigir a la misma página para que se muestre el producto agregado
    else:
        form = ProductoForm()

    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'productos/inventario.html', {'form': form, 'productos': productos})


def incrementar_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.stock += 1
    producto.save()
    return redirect('productos:lista_productos')

def disminuir_stock(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if producto.stock > 0:
        producto.stock -= 1
        producto.save()
    return redirect('productos:lista_productos')

def ventas_view(request):
    return render(request, 'productos/ventas.html')



@login_required
def registrar_venta_view(request):
    productos = Producto.objects.all()
    if request.method == "POST":
        # Procesar la cantidad ingresada por el usuario
        for producto in productos:
            cantidad_key = f'cantidad_{producto.id}'
            cantidad = request.POST.get(cantidad_key)

            if cantidad:
                cantidad = int(cantidad)

                if cantidad > 0:
                    # Crear una venta por cada producto y cantidad seleccionada
                    if producto.stock >= cantidad:
                        producto.stock -= cantidad  # Reduce el stock
                        producto.save()  # Guarda el cambio en el stock
                        Venta.objects.create(producto=producto, cantidad=cantidad, usuario=request.user)  # Crea la venta
                    else:
                        messages.error(request, f"No hay suficiente stock para {producto.nombre}.")

        return redirect('productos:ventas')
    else:
        form = VentaForm()

    # Mostrar las ventas recientes
    ventas = Venta.objects.all().order_by('-fecha')[:10]  # Las 10 ventas más recientes

    return render(request, 'productos/ventas.html', {'form': form, 'productos': productos, 'ventas': ventas})



@login_required
def registrar_venta(request):
    productos = Producto.objects.all()  # Obtén todos los productos
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            # Crear una venta por cada producto y cantidad seleccionada
            for producto_id, cantidad in form.cleaned_data['productos']:
                producto = Producto.objects.get(id=producto_id)
                if producto.stock >= cantidad:  # Verifica si hay suficiente stock
                    producto.stock -= cantidad  # Reduce el stock
                    producto.save()  # Guarda el cambio en el stock
                    Venta.objects.create(producto=producto, cantidad=cantidad)  # Crea la venta
                else:
                    form.add_error(None, f"No hay suficiente stock para {producto.nombre}.")
            return redirect('productos:ventas')  # Redirige a la página de ventas después de registrar
    else:
        form = VentaForm()

    # Mostrar las ventas recientes
    ventas = Venta.objects.all().order_by('-fecha')[:10]  # Las 10 ventas más recientes

    return render(request, 'productos/ventas.html', {'form': form, 'productos': productos, 'ventas': ventas})
