# productos/urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Ruta de login
    path('logout/', views.logout_view, name='logout'),  # Ruta de logout
    path('', views.login_view, name='home'),  # Ruta raíz que lleva al login
    path('inventario/', views.inventario_view, name='inventario'),  # Ruta al inventario
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('incrementar_stock/<int:producto_id>/', views.incrementar_stock, name='incrementar_stock'),
    path('disminuir_stock/<int:producto_id>/', views.disminuir_stock, name='disminuir_stock'),
    path('ventas/', views.registrar_venta_view, name='ventas'),
]


