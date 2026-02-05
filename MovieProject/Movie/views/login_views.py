from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render, redirect
from django.contrib import messages
from ..services.supabase_client import supabase
from django.contrib.auth import authenticate, login

User = get_user_model()



def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            response = supabase.table('users') \
                .select('user_id, name, password') \
                .eq('name', name) \
                .execute()

            users = response.data

            if not users:
                messages.error(request, 'ユーザーが見つかりません。')
                return render(request, 'login.html')

            user_data = users[0]

            if not check_password(password, user_data['password']):
                messages.error(request, 'パスワードが違います。')
                return render(request, 'login.html')

            # Djangoユーザー取得 or 作成
            django_user, created = User.objects.get_or_create(
                username=name,
                defaults={
                    "supabase_user_id": user_data["user_id"]
                }
            )

            # 🔴 ここ超重要
            django_user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, django_user)
            return redirect('latest_movies')

        except Exception as e:
            messages.error(request, f'ログインエラー: {e}')
            return render(request, 'login.html')

    return render(request, 'login.html')
