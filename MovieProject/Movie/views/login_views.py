from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import check_password
from ..services.supabase_client import supabase

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            # Supabaseでユーザー取得
            response = supabase.table('users').select('user_id,name,password').eq('name', name).execute()
            users = response.data
            print(f"[DEBUG] Supabase response: {users}")

            if not users:
                messages.error(request, 'ユーザーが見つかりません。')
                return render(request, 'login.html')

            user_data = users[0]

            # パスワードチェック
            if not check_password(password, user_data['password']):
                messages.error(request, 'パスワードが違います。')
                return render(request, 'login.html')

            # Djangoユーザー作成 or 取得
            django_user, created = User.objects.get_or_create(username=name)

            # Supabase ID 保存（カスタムフィールドがある場合）
            if created or not getattr(django_user, 'supabase_user_id', None):
                django_user.supabase_user_id = user_data['user_id']
                django_user.save()

            # ログイン
            login(request, django_user)
            return redirect('latest_movies')

        except Exception as e:
            messages.error(request, f"ログイン中にエラーが発生しました: {e}")
            return render(request, 'login.html')
        



    return render(request, 'login.html')
