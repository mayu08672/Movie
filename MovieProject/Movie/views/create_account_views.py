from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import make_password
from ..services.supabase_client import supabase

User = get_user_model()

def create_account(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        password = request.POST.get('user_password')

        if not name or not password:
            messages.error(request, '全ての項目を入力してください。')
            return render(request, 'create_account.html')

        # Supabase重複チェック
        existing_user = supabase.table('users').select('name').eq('name', name).execute()
        if existing_user.data:
            messages.error(request, 'このユーザー名は既に使われています。')
            return render(request, 'create_account.html')

        # パスワードハッシュ化
        hashed_password = make_password(password)

        # Supabase登録
        response = supabase.table('users').insert({
            'name': name,
            'password': hashed_password
        }).execute()

        supabase_user_id = response.data[0]['user_id']

        # Djangoユーザー作成（set_password 必須）
    django_user = User.objects.create_user(
    username=name,
    password=None  # ← Supabase管理なのでDjangoでは使わない
)

    django_user.supabase_user_id = supabase_user_id
    django_user.save()

# backend 明示
    django_user.backend = 'django.contrib.auth.backends.ModelBackend'

    login(request, django_user)

    return redirect('latest_movies')

    return render(request, 'create_account.html')
