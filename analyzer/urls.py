from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='analyzer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ログアウトのURLパターン
    path('', views.upload, name='upload'),  # デフォルトページ
    path('result/', views.result, name='result'),  # 結果表示ページ
]