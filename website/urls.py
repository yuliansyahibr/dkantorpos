from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('detail_product/', views.detail_product, name='detail_product'),
    path('kategori/', views.kategori, name='kategori'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('konfirmasi_pembayaran/', views.register, name='konfirmasi_pembayaran'),
]
