from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from . import models
from . import managers
import os

@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets = fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'hp', 'password1', 'password2',),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'hp')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        keranjang = models.Keranjang()
        keranjang.save()
        obj.keranjang = keranjang
        super(UserAdmin, self).save_model(request, obj, form, change)

class ProdukAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Produk._meta.fields]
    # list_display = ('id', 'jenis_item', 'kategori', 'nama_item', 'harga', 'deskripsi', 'jumlah_tersedia')
    list_filter = ('harga', 'stok', 'created_at', 'updated_at')
    actions = ['delete_selected']
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            os.remove(obj.foto.path)
            obj.delete()

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Order._meta.fields]
    # list_display = ('id', 'jenis_item', 'kategori', 'nama_item', 'harga', 'deskripsi', 'jumlah_tersedia')
    list_filter = ('user', 'total', 'status_pembayaran', 'created_at', 'uploaded_at')
    actions = ['delete_selected']
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            os.remove(obj.bukti_pembayaran.path)
            obj.delete()

admin.site.register(models.Kategori)
admin.site.register(models.Produk, ProdukAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Kantorpos)
admin.site.register(models.Properti)
admin.site.register(models.MetodePembayaran)
