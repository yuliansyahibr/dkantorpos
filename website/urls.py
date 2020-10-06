from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('item/<pk>', views.detail_product, name='detail_product'),
    path('kategori/', views.kategori, name='kategori'),
    path('keranjang/', views.keranjang, name='keranjang'),
    path('keranjang/ajax/<str:action>', views.keranjangAjax, name='keranjang_ajax'),
    path('api/<str:param>', views.api, name='api'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order, name='order'),
    path('thankyou/', views.thankyou, name='thankyou'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
