from django.db import models
from django.conf import settings
import os
import uuid
from django.utils.deconstruct import deconstructible


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

path_and_rename = PathAndRename("images/item")



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


class User(AbstractUser):
    """User model."""

    username = None
    # first_name = None
    # last_name = None
    # email = models.EmailField(_('email address'), unique=True)
    email = models.CharField(_('email'), unique=True, max_length=64)
    first_name = models.CharField(_('nama depan'), unique=True, max_length=64)
    last_name = models.CharField(_('nama belakang'), unique=True, max_length=64)
    password = models.CharField(_('password'), unique=True, max_length=64)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.UserManager()
 
    def __str__(self):
        if self.first_name == '':
            return self.email
        return self.first_name+' '+self.last_name


# class Profile(models.Model):
#     # Relations
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE,
#         related_name="profile")
#     alamat = models.CharField(max_length=32)
#     # Attributes - Optional
#     # Object Manager
#     objects = managers.ProfileManager()
 
#     # Custom Properties
#     @property
#     def username(self):
#         return self.user.username
 
#     # Methods
 
#     # Meta and String
#     class Meta:
#         verbose_name_plural = "profile"
#         ordering = ("user",)
 
#     def __str__(self):
#         return self.user.username

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile_for_new_user(sender, created, instance, **kwargs):
#     if created:
#         profile = Profile(user=instance)
#         profile.save()

class JenisItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis = models.CharField(max_length=32)

    def __str__(self):
        return self.jenis
    class Meta:
        verbose_name_plural = 'jenis item'

class Kategori(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=32)
    def __str__(self):
        return self.nama_kategori
    class Meta:
        verbose_name_plural = 'kategori'

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_file = models.CharField(max_length=64)
    # img = models.ImageField(upload_to=PathAndRename('images/item'))
    img = models.ImageField(upload_to=path_and_rename)
    # path = models.CharField(max_length=64)
    # tipe = models.CharField(max_length=64)
    # size = models.IntegerField()
    # height = models.IntegerField()
    # width = models.IntegerField()

    def __str__(self):
        return self.nama_file
    class Meta:
        verbose_name_plural = 'gambar'


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jenis_item = models.ForeignKey(
        JenisItem,
        on_delete=models.CASCADE
    )
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE
    )
    nama_item = models.CharField(max_length=32)
    harga = models.IntegerField()
    deskripsi = models.TextField()
    jumlah_tersedia = models.IntegerField()
    foto = models.ManyToManyField(Image)
    # foto = models.ImageField(upload_to=path_and_rename('images/item'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_item
    
    class Meta:
        verbose_name_plural = 'Item'


class Keranjang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        # Profile,
        on_delete=models.CASCADE,
    )
    total = models.IntegerField()

class IsiKeranjang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    keranjang = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        # Profile,
        on_delete=models.CASCADE,
    )
    item=models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaksi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        # Profile,
        on_delete=models.CASCADE
    )
    # metode_pembayaran
    subtotal = models.IntegerField()
    ongkos_kirim = models.IntegerField
    total = models.IntegerField()
    status_pembayaran = models.IntegerField()
    kecamatan_pengiriman = models.CharField(max_length=32)
    kota_pengiriman = models.CharField(max_length=32)
    alamat_pengiriman = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='transaksi'

class DetailTransaksi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaksi = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        # Profile,
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    qty = models.IntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    


# class Produk(models.Model):
#     kategori = models.ForeignKey(
#         Kategori,
#         on_delete=models.CASCADE
#     )
#     nama = models.CharField(max_length=64)
#     harga = models.IntegerField()
#     deskripsi = models.CharField(max_length=128)
#     jumlah = models.IntegerField()
#     foto = models.CharField(max_length=64)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Kantor(models.Model):
#     jenis = models.CharField(max_length=32)
#     deskripsi = models.CharField(max_length=128)
#     harga = models.IntegerField()
#     unit = models.IntegerField()
#     foto = models.CharField(max_length=64)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)