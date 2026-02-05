from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model
import bcrypt
from ..services.supabase_client import supabase

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")

        if not name or not password:
            messages.error(request, "ユーザー名とパスワードを入力してください。")
            return render(request, "login.html")

        try:
            # Supabase からユーザー取得
            response = (
                supabase
                .table("users")
                .select("user_id, name, password")
                .eq("name", name)
                .execute()
            )

            users = response.data or []

            if not users:
                messages.error(request, "ユーザーが見つかりません。")
                return render(request, "login.html")

            user_data = users[0]

            # Supabase ハッシュと bcrypt で照合
            if not bcrypt.checkpw(password.encode(), user_data["password"].encode()):
                messages.error(request, "パスワードが違います。")
                return render(request, "login.html")

            # Django ユーザー取得または作成
            django_user, created = User.objects.get_or_create(
                username=name,
                defaults={
                    "supabase_user_id": user_data["user_id"],
                    "is_active": True,
                }
            )

            if created:
                # Django でパスワードは無効化（Supabase 側で管理）
                django_user.set_unusable_password()
            django_user.is_active = True
            django_user.save()

            # backend 明示
            django_user.backend = "django.contrib.auth.backends.ModelBackend"

            # Django にログイン
            login(request, django_user)

            # 成功時は redirect
            return redirect("latest_movies")

        except Exception as e:
            messages.error(request, f"ログインエラー: {str(e)}")
            return render(request, "login.html")

    # GET 時は単純に表示
    return render(request, "login.html")
