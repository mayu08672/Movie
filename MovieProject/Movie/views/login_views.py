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
            # 🔹 Supabaseからユーザー取得
            response = (
                supabase
                .table("users")
                .select("user_id, name, password")
                .eq("name", name)
                .execute()
            )

            users = response.data

            if not users:
                messages.error(request, "ユーザーが見つかりません。")
                return render(request, "login.html")

            user_data = users[0]

            # 🔹 パスワード照合（Supabaseのハッシュ）
            if not check_password(password, user_data["password"]):
                messages.error(request, "パスワードが違います。")
                return render(request, "login.html")

            # 🔹 Djangoユーザー取得 or 作成
            try:
                django_user = User.objects.get(username=name)
            except User.DoesNotExist:
                django_user = User.objects.create(
                    username=name,
                    supabase_user_id=user_data["user_id"]
                )
                # 🔴 重要：Django側ではパスワードを使わない
                django_user.set_unusable_password()
                django_user.save()

            # 🔴 backend 明示（これがないとログイン保持されない）
            django_user.backend = "django.contrib.auth.backends.ModelBackend"

            # 🔹 ログイン
            login(request, django_user)

            # 🔹 成功時は必ず redirect
            return redirect("latest_movies")

        except Exception as e:
            messages.error(request, f"ログインエラー: {e}")
            return render(request, "login.html")

    return render(request, "login.html")
