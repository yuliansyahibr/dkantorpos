from website import models

def kategori(request):
    return {'daftar_kategori': models.Kategori.objects.all()}