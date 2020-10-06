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

def profile(request):
     return render(request, 'user/profile.html')

def updateTotal(keranjang):
     items = models.IsiKeranjang.objects.filter(keranjang=keranjang)
     #  update harga, sementara di luar if
     keranjang.total = sum([item.subtotal for item in items])
     keranjang.save()
def keranjangAjax(request, action):
     user = request.user
     keranjang = user.keranjang
     data = {}
     # print(request.POST)

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
               # update item keranjang di db
               item_keranjang = models.IsiKeranjang.objects.get(id=id_item_keranjang)
               item_keranjang.qty = new_qty
               item_keranjang.subtotal = item_keranjang.item.harga*item_keranjang.qty
               item_keranjang.save()

               data['qty'] = item_keranjang.qty
               data['subtotal'] = item_keranjang.subtotal
          else:
               return http.HttpResponseNotFound('Not Found')

          # update total di db
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

               if models.IsiKeranjang.objects.filter(keranjang=keranjang, item=item):
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

def checkout(request):
     user = request.user
     keranjang = user.keranjang
     # get isi keranjang
     items = models.IsiKeranjang.objects.filter(keranjang=keranjang)

     # if keranjang kosong, redirect
     if not items: 
          return http.HttpResponseRedirect('/')
     
     # flag item workspace di keranjang
     SEWA = True if 'workspace' in [str(item_keranjang.item.jenis_item).lower() for item_keranjang in items] else False
     request.session['SEWA'] = SEWA

     data = {
          'items': items,
          'total': keranjang.total,
          'provinsi': [] if SEWA else rajaOngkirAPI('provinsi'),
          'sewa': SEWA,
          'metode_pembayaran': models.MetodePembayaran.objects.all()
     }
     return render(request, 'checkout.html', data)

"""
api request
"""
def api(request, param):
     if request.method == 'POST':
          # result = rajaOngkirAPI(param, request.POST)
          result = rajaOngkirAPI(param, **request.POST)
          if result is not None:
               return http.JsonResponse(result, safe=False)
     return http.HttpResponseBadRequest()     
"""
doc: https://rajaongkir.com/dokumentasi/starter
"""
def rajaOngkirAPI(param, **kwargs):
     """
     Note: 
     request.POST values are list, get the 1st index [0] only
     """
     from http import client
     import ast, json
     
     # load api key
     API_KEY = ''
     with open('./website/rajaOngkir.json') as f:
          API_KEY = json.load(f)['API_KEY']
     
     # rajaOngkir api request
     conn = client.HTTPSConnection("api.rajaongkir.com")
     headers = { 'key': API_KEY }
     if param == 'provinsi':
          id_provinsi = kwargs.get('id_provinsi', "")
          conn.request("GET", "/starter/province?id={}".format(id_provinsi), headers=headers)
     elif param == 'kota':
          id_kota = kwargs.get('id_kota',"")
          if type(kwargs['id_provinsi']) == list:
               id_provinsi = kwargs['id_provinsi'][0]
          else:
               id_provinsi = kwargs['id_provinsi']
          conn.request("GET", "/starter/city?id={}&province={}".format(id_kota, id_provinsi), headers=headers)
     elif param == 'ongkir':
          if type(kwargs['id_kota']) == list:
               id_kota_tujuan = kwargs['id_kota'][0]
          else:
               id_kota_tujuan = kwargs['id_kota']
          headers['content-type'] = "application/x-www-form-urlencoded"
          id_kota_asal = '327' # ID KOTA PALEMBANG
          courier = 'pos' # kuris pos
          weight = 1400 # WEIGHT, hardcoded
          payload = "origin={}&destination={}&weight={}&courier={}".format(id_kota_asal, id_kota_tujuan, weight, courier)
          conn.request("POST", "/starter/cost", payload, headers)
     # get & decode api response
     res = conn.getresponse()
     data = res.read()
     data = ast.literal_eval(data.decode("utf-8"))

     if data['rajaongkir']['status']['code'] == 200:
          return data['rajaongkir']['results']
     return None

def order(request):
     if request.method == 'POST':
          print(request.POST)
          user = request.user
          keranjang = user.keranjang
          total =  keranjang.total
          data = {
               'user': request.user,
               'nama': request.POST['nama'],
               'telepon': request.POST['telepon'],
               'alamat': request.POST['alamat'],
               'metode_pembayaran': models.MetodePembayaran.objects.filter(id=request.POST['metode_pembayaran']).first(),
               'subtotal': total,
               'total': total,
               'status_pembayaran': 0,
          }
          if not request.session.get('SEWA', False):
               # Belum cek kosong
               id_provinsi = request.POST['id_provinsi']
               nama_provinsi = rajaOngkirAPI('provinsi', id_provinsi=id_provinsi)['province']
               id_kota = request.POST['id_kota']
               kota = rajaOngkirAPI('kota', id_provinsi=id_provinsi, id_kota=id_kota)
               nama_kota = kota['type']+' '+kota['city_name']
               service = request.POST['service']
               # cost = [d for d in rajaOngkirAPI('ongkir', id_kota=id_kota)[0]['costs'] if d['service'] == service]
               cost = next((x for x in rajaOngkirAPI('ongkir', id_kota=id_kota)[0]['costs'] if x['service'] == service), None)
               if cost is None:
                    return http.HttpResponseBadRequest()
               ongkos_kirim = cost['cost'][0]['value']
               estimasi = cost['cost'][0]['etd']
               data = {
                    **data,
                    'id_provinsi': id_provinsi,
                    'nama_provinsi': nama_provinsi,
                    'id_kota': id_kota,
                    'nama_kota': nama_kota,
                    'kodepos': request.POST['kodepos'],
                    'service': service,
                    'ongkos_kirim': ongkos_kirim,
                    'total': total+ongkos_kirim,
               }

          # save to db
          transaksi = models.Transaksi(**data)
          transaksi.save()

          request.session['id_transaksi'] = str(transaksi.id)
          request.session['total'] = transaksi.total

          del request.session['SEWA']
          request.session.modified = True
          
          print(data)
          print('==SAVED==')
          # return http.HttpResponseRedirect('/thankyou')
          return redirect('/thankyou', permanent=True)
     
     # return http.HttpResponseNotFound()

def thankyou(request):
     print('pesanan:', request.session.get('id_transaksi', ''))
     data = {
          'id_transaksi': request.session.get('id_transaksi', ''),
          'total': request.session.get('total', '')
     }
     return render(request, 'thankyou.html', data)

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