from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from ..services.supabase_client import supabase

def create_account(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        password = request.POST.get('user_password')

        if not name or not password:
            messages.error(request, '全ての項目を入力してください。')
            return render(request, 'create_account.html')

        # Supabaseで重複チェック
        try:
            existing = supabase.table('users').select('name').eq('name', name).execute()
            if existing.data and len(existing.data) > 0:
                messages.error(request, 'このユーザー名は既に使われています。')
                return render(request, 'create_account.html')
        except Exception as e:
            messages.error(request, f"ユーザー確認中にエラーが発生しました: {e}")
            return render(request, 'create_account.html')

        # パスワードをハッシュ化して登録
        hashed_password = make_password(password)
        try:
            supabase.table('users').insert({
                'name': name,
                'password': hashed_password
            }).execute()
        except Exception as e:
            messages.error(request, f"登録中にエラーが発生しました: {e}")
            return render(request, 'create_account.html')

        messages.success(request, 'アカウント作成成功！ログインしてください。')
        return redirect('login')

    return render(request, 'create_account.html')
