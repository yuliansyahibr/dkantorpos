from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from . import models
from .models import Kategori 
from .models import JenisItem, Item 
from .models import Keranjang, IsiKeranjang 
from .models import Transaksi, DetailTransaksi


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
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class ItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Item._meta.fields]
    # list_display = ('id', 'jenis_item', 'kategori', 'nama_item', 'harga', 'deskripsi', 'jumlah_tersedia')
    list_filter = ('harga', 'jumlah_tersedia', 'created_at', 'updated_at')

admin.site.register(Kategori)
admin.site.register(JenisItem)
admin.site.register(Item, ItemAdmin)
admin.site.register(Transaksi)
# admin.site.register(DetailTransaksi)
# admin.site.register(Keranjang)
# admin.site.register(IsiKeranjang)
