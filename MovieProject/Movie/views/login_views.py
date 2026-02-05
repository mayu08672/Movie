from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import check_password
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

            # Supabaseのハッシュと照合
            if not check_password(password, user_data["password"]):
                messages.error(request, "パスワードが違います。")
                return render(request, "login.html")

            # Djangoユーザー取得 or 作成
            django_user, created = User.objects.get_or_create(
                username=name,
                defaults={
                    "supabase_user_id": user_data["user_id"],
                    "is_active": True,   # ← ここ超重要
                }
            )

            if created:
                django_user.set_unusable_password()

            # 既存ユーザーでも念のため有効化
            django_user.is_active = True
            django_user.save()

            # backend 明示（これがないと login() が無効）
            django_user.backend = "django.contrib.auth.backends.ModelBackend"

            login(request, django_user)

            # 成功時は必ず redirect
            return redirect("latest_movies")

        except Exception as e:
            messages.error(request, f"ログインエラー: {e}")
            return render(request, "login.html")

    return render(request, "login.html")
