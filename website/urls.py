from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('produk/<str:pk>', views.detail_product, name='detail_product'),
    path('properti/<str:pk>', views.detail_properti, name='detail_properti'),
	path('success/', views.success, name='success'),
    # path('item/<uuid:pk>', views.detail_product, name='detail_product'),
    # path('kategori/<str:nama_kategori>', views.kategori_list, name='kategori'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('profil/', views.profil, name='profil'),
    path('register/', views.register, name='register'),
    # path('kategori/', views.kategori, name='kategori'),
	path('search/',views.search_product, name='search'),
    path('keranjang/', views.keranjang, name='keranjang'),
    path('keranjang/ajax/<str:action>', views.keranjangAjax, name='keranjang_ajax'),
    # path('api/<str:param>', views.api, name='api'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.makeorder, name='order'),
	path('sendEmail/', views.sendEmail, name='sendEmail'),
    path('terimakasih/', views.terimakasih, name='terimakasih'),
    path('konfirmasi-pembayaran/<str:id_order>', views.konfirmasi_pembayaran, name='konfirmasi_pembayaran'),
    path('daftar-transaksi/', views.daftar_transaksi, name='daftar_transaksi'),
    path('konfirmasi-email/', views.konfirmasi_email, name='konfirmasi_email'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate_account, name='activate'),
    path('b/<str:jenis>', views.browse, name='browse'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
