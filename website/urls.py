from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    #	path('produk/<uuid:id_item>', views.produk, name='produk'),
    path('item/<uuid:pk>', views.detail_product, name='detail_product'),
	path('benda_pos_list/', views.kategori_list, kwargs={'kategori': 'Materai'}, name='benda_pos_list'),
    path('co_working_list/', views.kategori_list, kwargs={'kategori': 'Workspace'}, name='co_working_list'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
	path('search/',views.search_product, name='search'),
    path('keranjang/', views.keranjang, name='keranjang'),
    path('keranjang/ajax/<str:action>', views.keranjangAjax, name='keranjang_ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
