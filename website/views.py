from django.contrib.auth import login as authlogin, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm
from . import models
from .models import Produk
from .models import Properti
from django import http
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import uuid

def index(request):
     shelf_barang = Produk.objects.order_by('-created_at').all()[:6]
     shelf_workspace = Properti.objects.order_by('-created_at').all()[:4]
	#	request.session.flush()
     data = {
          'shelf_barang': shelf_barang,
          'shelf_workspace': shelf_workspace
     }
     return render(request, 'index.html', data)

def register(request):
     if request.user.is_authenticated:
          return http.HttpResponseRedirect('/')
     if request.method == 'POST':
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
          form = SignUpForm()
     return render(request, 'registration/register.html', {'form': form})

@login_required
def profil(request):
     return render(request, 'user/profil.html')

def detail_product(request, pk):	
    try:
        item = Produk.objects.get(pk=pk)
    except Produk.DoesNotExist:
        raise http.Http404('Produk tidak ditemukan.')    
    return render(request, 'detail_product.html', {'item': item})

def detail_properti(request, pk):
    try:
        item = Properti.objects.get(pk=pk)
    except Properti.DoesNotExist:
        raise http.Http404('Properti tidak ditemukan.')    
    return render(request, 'detail_properti.html', {'item': item})

def detail_properti2(request, pk):
    try:
        item = Properti.objects.get(pk=pk)
    except Properti.DoesNotExist:
        raise http.Http404('Properti tidak ditemukan.')    
    return render(request, 'detail_product.html', {'item': item})

def kategori_list(request, nama_kategori):
    item_list = models.Produk.objects.filter(kategori__nama_kategori=nama_kategori)
	
    return render(request,'index.html', {'item_list': item_list})
	
""" search function  """
def search_product(request):
    if request.method == "POST":
          query_name = request.POST.get('name', None)
          if query_name:
               # contains => case sensitive
               # icontains => case insensitive
               results1 = Produk.objects.filter(nama_produk__icontains=query_name).all()
               results2 = Properti.objects.filter(nama__icontains=query_name).all()
               return render(request, 'product_search.html', {"results1":results1, "results2":results2})

    return render(request, 'product_search.html')

def updateKeranjang(keranjang):
     items = models.IsiKeranjang.objects.filter(keranjang=keranjang)
     #  update harga, sementara di luar if
     keranjang.total = sum([item.subtotal for item in items])
     keranjang.jumlah_item = sum([item.qty for item in items])
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

               print(new_qty, item_keranjang.produk.stok)

               if new_qty >=  item_keranjang.produk.stok:
                    return http.HttpResponseServerError('Error')

               item_keranjang.qty = new_qty
               item_keranjang.subtotal = item_keranjang.produk.harga*item_keranjang.qty
               item_keranjang.save()

               data['qty'] = item_keranjang.qty
               data['subtotal'] = item_keranjang.subtotal
          else:
               return http.HttpResponseNotFound('Not Found')

          # update total di db
          updateKeranjang(keranjang)

          data['status']= 200
          data['total']= item_keranjang.keranjang.total
          data['jumlah_item']= item_keranjang.keranjang.jumlah_item

          return http.JsonResponse(data)

def checkQty():
     pass

@login_required
def keranjang(request):
     request.session['keranjang'] = True
     user = request.user
     keranjang = user.keranjang
     if request.method == 'POST':
          # Update/Add item keranjang
          if request.POST['action'] == 'add':
               id_item = request.POST['id_item']
               item = models.Produk.objects.get(id=id_item)
               qty = int(request.POST['qty'])
               if item is None:
                    return http.HttpResponseNotFound()
               # jika item workspace
               # if item._meta.model_name == 'properti':
               #      request.session['WORKSPACE'] = True
               #      request.session['id_item'] = id_item
               #      return http.HttpResponseRedirect('/checkout')
               if qty >= item.stok:
                    return http.HttpResponseBadRequest()

               if models.IsiKeranjang.objects.filter(keranjang=keranjang, produk=item):
                    item_keranjang = models.IsiKeranjang.objects.filter(keranjang=keranjang, produk=item).first()
                    item_keranjang.qty += qty
                    if item_keranjang.qty >= item.stok:
                         return http.HttpResponseBadRequest()
                    item_keranjang.subtotal = item.harga*item_keranjang.qty
                    item_keranjang.save()
               else:
                    item_keranjang = models.IsiKeranjang(keranjang=keranjang, produk=item, qty=qty, subtotal=item.harga*qty)
                    item_keranjang.save()
               
               updateKeranjang(keranjang)
               
               return http.HttpResponseRedirect('/keranjang')
     items = models.IsiKeranjang.objects.filter(keranjang=keranjang)
     data = {
          'items': items,
          'keranjang': keranjang,
     }
     return render(request, 'keranjang.html', data)

"""return object yg sama seperti itemkeranjang model obj"""
def get_item_keranjang_workspace(id_item, qty=1):
     if id_item is None:
          return None
     from collections import namedtuple
     item = models.Properti.objects.get(id=id_item)
     # IsiKeranjang = namedtuple('IsiKeranjang', ['item','qty','subtotal'])
     args = {'item':item, 'qty':qty, 'subtotal':item.harga}
     return models.IsiKeranjang(**args)
     
@login_required
def checkout(request):
     WORKSPACE = request.session.get('WORKSPACE')
     if WORKSPACE:
          item_keranjang = get_item_keranjang_workspace(request.session.get('id_item'))
          items = [item_keranjang]
          keranjang = {'total':item_keranjang.produk.harga, 'jumlah_item':item_keranjang.qty}
          kantorpos = []
          provinsi = []
     else:
          user = request.user
          keranjang = user.keranjang
          items = models.IsiKeranjang.objects.filter(keranjang=keranjang)
          # if keranjang kosong, redirect
          if not items: 
               return http.HttpResponseRedirect('/keranjang')
          # provinsi = rajaOngkirAPI('provinsi')
          kantorpos = models.Kantorpos.objects.all()
          provinsi = []
     
     # flag item workspace di keranjang
     # SEWA = True if 'workspace' in [str(item_keranjang.produk.jenis_item.jenis).lower() for item_keranjang in items] else False
     # request.session['SEWA'] = SEWA

     data = {
          'items': items,
          'keranjang': keranjang,
          'provinsi': provinsi,
          'WORKSPACE': WORKSPACE,
          'kantorpos': kantorpos,
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
     request.POST values are in list, get the 1st index [0] only
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

@login_required
def makeorder(request):
     if request.method == 'POST':
          # print(request.POST)
          user = request.user
          # return http.HttpResponseForbidden()

          WORKSPACE = request.session.get('WORKSPACE')
          if WORKSPACE:
               id_item = request.session.get('id_item')
               item_keranjang = get_item_keranjang_workspace(request.session.get('id_item'))
               # items = [item_keranjang]
               keranjang = models.Keranjang(**{'total':item_keranjang.produk.harga, 'jumlah_item':item_keranjang.qty})
               _data = {
                    'total': keranjang.total
               }
          else:
               keranjang = user.keranjang
               # Belum cek kosong

               #################### ONGKIR
               # id_provinsi = request.POST['id_provinsi']
               # nama_provinsi = rajaOngkirAPI('provinsi', id_provinsi=id_provinsi)['province']
               # id_kota = request.POST['id_kota']
               # kota = rajaOngkirAPI('kota', id_provinsi=id_provinsi, id_kota=id_kota)
               # nama_kota = kota['type']+' '+kota['city_name']
               # service = request.POST['service']
               # # cost = [d for d in rajaOngkirAPI('ongkir', id_kota=id_kota)[0]['costs'] if d['service'] == service]
               # cost = next((x for x in rajaOngkirAPI('ongkir', id_kota=id_kota)[0]['costs'] if x['service'] == service), None)
               # if cost is None:
               #      return http.HttpResponseBadRequest()
               # ongkos_kirim = cost['cost'][0]['value']
               # estimasi = cost['cost'][0]['etd']
               ##################
               # kurir = request.POST['kurir']
               kurir = "pos"
               ongkos_kirim = 10000 # HARDCODE
               kantorpos = models.Kantorpos.objects.filter(id=request.POST['kantorpos']).first()
               metode_pembayaran = models.MetodePembayaran.objects.filter(id=request.POST['metode_pembayaran']).first()

               _data = {
                    # 'id_provinsi': id_provinsi,
                    # 'nama_provinsi': nama_provinsi,
                    # 'id_kota': id_kota,
                    # 'nama_kota': nama_kota,
                    # 'kodepos': request.POST['kodepos'],
                    # 'service': service,
                    
                    'ongkos_kirim': ongkos_kirim,
                    'total': keranjang.total+ongkos_kirim,
                    # 'kurir': kurir,
                    'kantorpos': kantorpos,
                    'metode_pembayaran': metode_pembayaran,
               }

          data = {
               'kode': uuid.uuid4().hex[:12].upper(),
               'user': request.user,
               'nama_penerima': request.POST['nama'],
               'telepon_penerima': request.POST['telepon'],
               'alamat_pengiriman': request.POST['alamat'],
               'subtotal': keranjang.total,
               'status_pembayaran': 0,
               'jumlah_item': keranjang.jumlah_item,
               **_data
          }

          # if WORKSPACE is None:
          #      # Belum cek kosong
          #      id_provinsi = request.POST['id_provinsi']
          #      nama_provinsi = rajaOngkirAPI('provinsi', id_provinsi=id_provinsi)['province']
          #      id_kota = request.POST['id_kota']
          #      kota = rajaOngkirAPI('kota', id_provinsi=id_provinsi, id_kota=id_kota)
          #      nama_kota = kota['type']+' '+kota['city_name']
          #      service = request.POST['service']
          #      # cost = [d for d in rajaOngkirAPI('ongkir', id_kota=id_kota)[0]['costs'] if d['service'] == service]
          #      cost = next((x for x in rajaOngkirAPI('ongkir', id_kota=id_kota)[0]['costs'] if x['service'] == service), None)
          #      if cost is None:
          #           return http.HttpResponseBadRequest()
          #      ongkos_kirim = cost['cost'][0]['value']
          #      estimasi = cost['cost'][0]['etd']
          #      data = {
          #           **data,
          #           'id_provinsi': id_provinsi,
          #           'nama_provinsi': nama_provinsi,
          #           'id_kota': id_kota,
          #           'nama_kota': nama_kota,
          #           'kodepos': request.POST['kodepos'],
          #           'service': service,
          #           'ongkos_kirim': ongkos_kirim,
          #           'total': total+ongkos_kirim,
          #      }

          # save to db
          order = models.Order(**data)
          order.save()
          for item in models.IsiKeranjang.objects.filter(keranjang=keranjang).all():
               detail_order = models.DetailOrder(order=order)
               detail_order.produk = item.produk
               detail_order.qty = item.qty
               detail_order.subtotal = item.subtotal
               detail_order.save()

               produk = detail_order.produk
               produk.stok -= detail_order.qty
               if(produk.stok < 0):
                    produk.stop = 0
               produk.save()

          if WORKSPACE:
               del request.session['WORKSPACE']
               del request.session['id_item']
               request.session.modified = True
          else:
               # RESET KERANJANG
               models.IsiKeranjang.objects.filter(keranjang=keranjang).all().delete()
               keranjang.total=0
               keranjang.jumlah_item=0
               keranjang.save()

          request.session['id_order'] = order.id.hex
          request.session['total'] = order.total
          
          print(data)
          print('==SAVED==')
          return http.HttpResponseRedirect('/terimakasih')
          # return redirect('/terimakasih', permanent=True)
     
     # return http.HttpResponseNotFound()

@login_required
def terimakasih(request):
     from datetime import timedelta

     id_order = request.session.get('id_order', '')
     order = models.Order.objects.filter(id=id_order).first()
     waktu_sampai = order.created_at
     # print(waktu_sampai)
     waktu_sampai += timedelta(days=3)
     # print(waktu_sampai)
     metode = order.metode_pembayaran.nama_metode
     data = {
          'order': order,
          'metode': metode,
          'waktu_sampai': waktu_sampai,
          'total': request.session.get('total', ''),
          'form': forms.KonfirmasiPembayaranForm()
     }
     return render(request, 'terimakasih.html', data)

@login_required
def konfirmasi_pembayaran(request, id_order):
     if request.method == 'POST':
          # print('POST')
          user = request.user
          # print(request.FILES)
          form = forms.KonfirmasiPembayaranForm(request.POST, request.FILES)
          if form.is_valid():
               from django.utils import timezone
               img = form.cleaned_data.get('bukti_pembayaran')
               order = models.Order.objects.filter(id=id_order).first()
               order.bukti_pembayaran = img
               now = timezone.now()
               print(now)
               order.uploaded_at = now
               order.status_pembayaran = 1
               order.save()
               return http.HttpResponseRedirect('/daftar-transaksi')
@login_required
def daftar_transaksi(request):
     user = request.user
     orders = models.Order.objects.filter(user=user).order_by('-created_at').all()
     for order in orders:
          order.details = models.DetailOrder.objects.filter(order=order).all()
     # print(orders[1].detail)
     data = {
          'orders': orders,
          'form': forms.KonfirmasiPembayaranForm()
     }
     return render(request, 'daftar_transaksi.html', data)

def contact(request):
    return render(request, "contact.html")
	
def sendEmail(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        from_email = request.POST['email']
        message = request.POST['message']
        try:
            send_mail(subject, message, from_email, ['dkantorpos01@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/contact') # Redirect Sementara Ketika Berhasil Kirim Pesan

def success(request):
    return HttpResponse('Success! Thank you for your message.')

def kategori(request):
     return render(request, 'kategoribendapos.html')