from django.contrib.auth import login as authlogin, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from . import models
from .models import Item
from django import http
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import numpy as np

def index(request):
    shelf = Item.objects.all()
	#	request.session.flush()
    return render(request, 'index.html', {'shelf': shelf})

def register(request):
     if request.method == 'POST':
     #    form = UserCreationForm(request.POST)
     #    if form.is_valid():
     #        form.save()
     #        username = form.cleaned_data.get('username')
     #        raw_password = form.cleaned_data.get('password1')
     #        user = authenticate(username=username, password=raw_password)
     #        authlogin(request, user)
     #        return redirect('index')
          form = SignUpForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               keranjang = models.Keranjang(total=0)
               keranjang.save()
               user.keranjang = keranjang
               user.save()
               form.save_m2m()

               # username = form.cleaned_data.get('username')
               email = form.cleaned_data.get('email')
               raw_password = form.cleaned_data.get('password1')
               user = authenticate(username=email, password=raw_password)
               authlogin(request, user)
               return redirect('index')
     else:
     # form = UserCreationForm()
          form = SignUpForm()
     # return render(request, 'registered.html')
          return render(request, 'registration/register.html', {'form': form})

# def produk(request, id_item):
     # item = models.Item.objects.get(id=id_item)
     # data = {
          # 'item': item
     # }
     # return render(request, 'produk.html', data)

def updateTotal(keranjang):
     items = models.IsiKeranjang.objects.filter(keranjang=keranjang)
     #  update harga, sementara di luar if
     keranjang.total = np.sum([item.subtotal for item in items])
     keranjang.save()

def keranjangAjax(request, action):
     user = request.user
     keranjang = user.keranjang
     data = {}
     print(request.POST)

     if request.method == 'POST':
          # Hapus item keranjang
          if action == 'delete':
               id_item_keranjang = request.POST['id_item_keranjang']
               item_keranjang = models.IsiKeranjang.objects.get(id=id_item_keranjang)
               item_keranjang.delete()

          # Update qty
          elif action == 'update_qty':
               id_item_keranjang = request.POST['id_item_keranjang']
               new_qty = int(request.POST['qty'])

               # Validate quantity
               # return error jika qty kurang dari 1
               if new_qty < 1:
                    return http.HttpResponseServerError('Error')

               item_keranjang = models.IsiKeranjang.objects.get(id=id_item_keranjang)
               item_keranjang.qty = new_qty
               item_keranjang.subtotal = item_keranjang.item.harga*item_keranjang.qty
               item_keranjang.save()

               data['qty'] = item_keranjang.qty
               data['subtotal'] = item_keranjang.subtotal
          else:
               return http.HttpResponseNotFound('Not Found')

          updateTotal(keranjang)

          data['status']= 200
          data['total']= item_keranjang.keranjang.total

          return JsonResponse(data)

def keranjang(request):
     user = request.user
     keranjang = user.keranjang

     if request.method == 'POST':
          # Update/Add item keranjang
          if request.POST['action'] == 'add':
               id_item = request.POST['id_item']
               item = models.Item.objects.get(id=id_item)
               qty = int(request.POST['qty'])

               if models.IsiKeranjang.objects.filter(keranjang=keranjang, item=id_item):
                    item_keranjang = models.IsiKeranjang.objects.filter(keranjang=keranjang, item=item).first()
                    item_keranjang.qty += qty
                    item_keranjang.subtotal = item.harga*item_keranjang.qty
                    item_keranjang.save()
               else:
                    item_keranjang = models.IsiKeranjang(keranjang=keranjang, item=item, qty=qty, subtotal=item.harga*qty)
                    item_keranjang.save()
               
               updateTotal(keranjang)

               return HttpResponseRedirect('/keranjang')

     items = models.IsiKeranjang.objects.filter(keranjang=keranjang)

     data = {
          'items': items,
          'total': keranjang.total
     }

     return render(request, 'keranjang.html', data)

def profile(request):
     return render(request, 'user/profile.html')
     
def checkout(request):
    return render(request, 'checkout.html')

def contact(request):
    return render(request, 'contact.html')

def kategori(request):
     return render(request, 'kategoribendapos.html')

def detail_product(request, pk):			
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        raise http.Http404('Item does not exist')
    
    return render(request, 'detail_product.html', {'item': item})

def kategori_list(request, kategori):
    item_list = models.Item.objects.filter(kategori__nama_kategori=kategori)
	
    return render(request,'index.html', {'item_list': item_list})
	
def search_product(request):
    #	""" search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Item.objects.filter(nama_item__contains=query_name)
            return render(request, 'product_search.html', {"results":results})

    return render(request, 'product_search.html')