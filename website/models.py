from django.db import models
from django.conf import settings
import os
import uuid
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

"""
    FUNCTIONS
"""
@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)
# path_and_rename = PathAndRename("images/item")

IMAGE_SIZE_LIMIT = 3 #Mb
def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = IMAGE_SIZE_LIMIT
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

"""
    Custom Fields
"""
class CustomEmailField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(CustomEmailField, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).lower()

""" 
    MODELS
"""
from . import managers
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Kantorpos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kode = models.CharField(max_length=8, null=True)
    regional = models.CharField(max_length=2, null=True)
    nama = models.CharField(max_length=32, null=True)
    def __str__(self):
        return 'Kantor pos '+self.nama
    class Meta:
        verbose_name_plural = 'kantor pos'

class Keranjang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jumlah_item = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

class User(AbstractUser):
    """User model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    # first_name = None
    # last_name = None

    email = CustomEmailField(_('email'), unique=True, max_length=64)
    # uncomment kode dibawah supaya email jadi char, untuk mempermudah register/login
    # email = models.CharField(_('email'), unique=True, max_length=64)
    first_name = models.CharField(_('nama depan'), max_length=64)
    last_name = models.CharField(_('nama belakang'), max_length=64, null=True, blank=True)
    hp = models.CharField(_('hp'), max_length=14)
    password = models.CharField(_('password'), max_length=64)

    keranjang = models.ForeignKey(
        Keranjang,
        default=None,
        on_delete=models.CASCADE,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()
 
    def __str__(self):
        if self.first_name == '':
            return self.email
        return self.first_name+' '+ (self.last_name if self.last_name else '')
    # def delete(self):
    #     self.foto.delete()
    #     super(User, self).delete()

class Kategori(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=32)
    def __str__(self):
        return self.nama_kategori
    class Meta:
        verbose_name_plural = 'kategori'


class Produk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE
    )
    nama_produk = models.CharField(max_length=32)
    harga = models.IntegerField()
    deskripsi = models.TextField(null=True)
    stok = models.IntegerField()
    # foto = models.ImageField()
    path_and_rename = PathAndRename("images/produk")
    help_text = 'Maximum file size allowed is {}Mb'.format(IMAGE_SIZE_LIMIT)
    foto = models.ImageField("Foto produk", upload_to=path_and_rename, validators=[validate_image], help_text=help_text)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_produk
    def delete(self):
        # self.foto.delete()
        if os.path.isfile(self.foto.path):
            os.remove(self.foto.path)
        super(self, Produk).delete()
    
    class Meta:
        verbose_name_plural = 'Produk'

class IsiKeranjang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keranjang = models.ForeignKey(
        Keranjang,
        on_delete=models.CASCADE,
    )
    produk=models.ForeignKey(
        Produk,
        on_delete=models.CASCADE,
    )
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MetodePembayaran(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # kode = models.CharField(max_length=16)
    nama_metode = models.CharField(max_length=32)
    deskripsi = models.CharField(max_length=128)
    def __str__(self):
        return self.nama_metode
    class Meta:
        verbose_name_plural='metode pembayaran'

class Alamat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kode = models.CharField(max_length=16, unique=True)
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        on_delete=models.CASCADE
    )
    metode_pembayaran = models.ForeignKey(
        MetodePembayaran,
        on_delete=models.CASCADE
    )
    nama_penerima = models.CharField(max_length=64)
    telepon_penerima = models.CharField(max_length=64)
    alamat_pengiriman = models.CharField(max_length=64)
    subtotal = models.IntegerField()
    ongkos_kirim = models.IntegerField(null=True)
    total = models.IntegerField()
    # status_pembayaran = models.IntegerField()
    BELUM_BAYAR = 0
    SUDAH_BAYAR = 1
    SUDAH_VERIFIKASI = 2
    CHOICES = [
        (BELUM_BAYAR, 'Belum dibayar'),
        (SUDAH_BAYAR, 'Sudah dibayar, belum diverfikasi'),
        (SUDAH_VERIFIKASI, 'Sudah diverifikasi'),
    ]
    status_pembayaran = models.IntegerField(
        # max_length=1,
        choices=CHOICES,
        default=BELUM_BAYAR,
    )
    jumlah_item = models.IntegerField(default=0)

    kantorpos = models.ForeignKey(
        Kantorpos,
        on_delete=models.CASCADE
    )
    # kodepos = models.CharField(max_length=6, null=True)
    # id_kota = models.IntegerField(null=True)
    # id_provinsi = models.IntegerField(null=True)
    # nama_kota = models.CharField(max_length=32, null=True)
    # nama_provinsi = models.CharField(max_length=32, null=True)
    
    # kurir = models.CharField(max_length=32, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    path_and_rename = PathAndRename("images/bukti_pembayaran")
    help_text = 'Maximum file size allowed is {}Mb'.format(IMAGE_SIZE_LIMIT)
    bukti_pembayaran = models.ImageField(upload_to=path_and_rename, null=True, validators=[validate_image], help_text=help_text, )
    uploaded_at = models.DateTimeField(null=True)

    def delete(self):
        # self.bukti_pembayaran.delete()
        if os.path.isfile(self.bukti_pembayaran.path):
            os.remove(self.bukti_pembayaran.path)
        super(Order, self).delete()
    class Meta:
        verbose_name_plural='order'

class DetailOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE
    )
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Properti(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kode = models.CharField(max_length=16, unique=True)
    nama = models.CharField(max_length=64)
    deskripsi = models.TextField()
    alamat = models.CharField(max_length=128)
    # lebar = models.IntegerField()
    # panjang = models.IntegerField()
    luas_tanah = models.IntegerField() #m2
    luas_bangunan = models.IntegerField() #m2
    lantai = models.IntegerField()
    listrik = models.IntegerField()
    harga = models.IntegerField()

    kantropos = models.ForeignKey(
        Kantorpos, on_delete=models.CASCADE
    )
    TIDAK_ADA = 0
    ADA = 1
    CHOICES = [
        (TIDAK_ADA, 'Tidak ada'),
        (ADA, 'Ada')
    ]
    ketersediaan = models.IntegerField(
        choices=CHOICES,
        default=ADA,
    )

    path_and_rename = PathAndRename("images/properti")
    help_text = 'Maximum file size allowed is {}Mb'.format(IMAGE_SIZE_LIMIT)
    foto = models.ImageField("Foto properti", upload_to=path_and_rename, validators=[validate_image], help_text=help_text)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
    def delete(self):
        # self.foto.delete()
        if os.path.isfile(self.foto.path):
            os.remove(self.foto.path)
        super(Properti, self).delete()
    
    class Meta:
        verbose_name_plural = 'Properti'

class permintaan_sewa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        User, models.CASCADE
    )
    nama = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    telepon = models.CharField(max_length=64)
    instansi = models.CharField(max_length=64, null=True)
    catatan = models.CharField(max_length=64, null=True)
    
    properti = models.ForeignKey(
        Properti, models.CASCADE
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

