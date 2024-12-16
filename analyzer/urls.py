from django.contrib import admin
from django.urls import path
from . import views #views.pyから関数をインポート

urlpatterns = [
    path('',views.upload, name="upload"), # ルートURLをviews.uploadに紐づける
]