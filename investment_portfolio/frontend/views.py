from django.shortcuts import render, redirect, get_object_or_404
from api.models import User, Asset
from django.contrib import messages
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        balance = request.POST.get('balance', 0)

        if User.objects.filter(name=name).exists():
            messages.error(
                request,
                "Пользователь с таким именем уже существует."
            )
            return redirect('register')

        User.objects.create(name=name, password=password, balance=balance)
        messages.success(
            request,
            "Регистрация прошла успешно! Войдите в аккаунт."
        )
        return redirect('/login')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(name=name, password=password)
            messages.success(request, f"Добро пожаловать, {user.name}!")
            return redirect(f'/profile/{user.id}/')
        except User.DoesNotExist:
            messages.error(request, "Неверное имя пользователя или пароль.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    assets = Asset.objects.filter(user_id=user_id)
    return render(request, 'index.html', {'user': user, 'assets': assets})


def delete_asset(request, user_id, asset_id):
    asset = get_object_or_404(Asset, id=asset_id, user_id=user_id)
    asset.delete()
    messages.success(request, f'Актив "{asset.coin_name}" был успешно удален.')
    return redirect('profile', user_id=user_id)


def add_asset(request, user_id):
    if request.method == 'POST':
        coin_name = request.POST.get('coin_name')
        quantity = request.POST.get('quantity')
        value_rub = request.POST.get('value_rub')
        asset = Asset.objects.create(
            coin_name=coin_name,
            quantity=quantity,
            value_rub=value_rub,
            user_id=user_id
        )
        messages.success(request, f'Актив "{coin_name}" успешно добавлен.')
        return redirect('profile', user_id=user_id)
    return render(request, 'profile.html')
