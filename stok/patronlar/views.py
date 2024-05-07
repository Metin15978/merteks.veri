from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import *
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Giriş görünümü
@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # Kullanıcı doğrulama başarısız olduğunda hata mesajı göstermek
            return render(request, 'login.html', {'error_message': 'Kullanıcı adı veya şifre yanlış'})
    # GET isteği durumunda veya doğrulama başarısız olduğunda login.html şablonunu render et
    return render(request, 'login.html')

# Çıkış görünümü
@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

# Ana sayfa görünümü
@login_required
def home(request):
    order_by = request.GET.get('order_by', '-tarih')
    firmalar = Firmalar.objects.all()
    firmalar = firmalar.order_by(order_by)
    paginator = Paginator(firmalar, 8)  # Sayfalama için Paginator oluşturun, her sayfada 4 öğe gösterilecek
    page_number = request.GET.get('page')
    try:
        firmalar = paginator.page(page_number)
    except PageNotAnInteger:
        # Eğer page sayısal bir değer değilse, ilk sayfayı getir
        firmalar = paginator.page(1)
    except EmptyPage:
        # Eğer page, mevcut sayfalama aralığının dışındaysa, son sayfayı getir
        firmalar = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'firmalar': firmalar})

# İNDEX
def index(request):
    return render(request, 'index.html')

# SEACRH
def search(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', '-tarih')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    firmalar = Firmalar.objects.all()
    
    if query:
        firmalar = firmalar.filter(
            Q(firma_adi__icontains=query) |
            Q(Adet__icontains=query) |
            Q(sha__icontains=query) |
            Q(cinsi_2__icontains=query) |
            Q(cinsi_1__icontains=query) |
            Q(renk__icontains=query) |
            Q(demir_capi__icontains=query) |
            Q(temiz_capi__icontains=query) |
            Q(boy__icontains=query) |
            Q(durumu__icontains=query) |
            Q(not_bilgisi__icontains=query)
        )
    
    # DATAYI FİLTRELE
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            firmalar = firmalar.filter(tarih__range=(start_date, end_date))
        except ValueError:
            pass  
    
    # SORGU SIRALAMA
    firmalar = firmalar.order_by(order_by)

    return render(request, 'home.html', {'firmalar': firmalar})

