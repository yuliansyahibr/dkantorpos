from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('detail_product/', views.detail_product, name='detail_product'),
    path('kategori/', views.kategori, name='kategori'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
