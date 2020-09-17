from django.contrib.auth import login as authlogin, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Item
from django.http import HttpResponse

def index(request):
    shelf = Item.objects.all()
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
               form.save()
               # username = form.cleaned_data.get('username')
               email = form.cleaned_data.get('email')
               raw_password = form.cleaned_data.get('password1')
               user = authenticate(username=email, password=raw_password)
               authlogin(request, user)
               return redirect('index')
     else:
     #    form = UserCreationForm()
          form = SignUpForm()
     # return render(request, 'registered.html')
     return render(request, 'registration/register.html', {'form': form})

def checkout(request):
     return render(request, 'checkout.html')

def contact(request):
     return render(request, 'contact.html')

def detail_product(request):
     return render(request, 'detail_product.html')

def kategori(request):
     return render(request, 'kategoribendapos.html')

