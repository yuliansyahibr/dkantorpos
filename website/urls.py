from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('produk/<uuid:id_item>', views.produk, name='produk'),
    path('item/<pk>', views.detail_product, name='detail_product'),
    path('kategori/', views.kategori, name='kategori'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('keranjang/', views.keranjang, name='keranjang'),
    path('keranjang/ajax/<str:action>', views.keranjangAjax, name='keranjang_ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
