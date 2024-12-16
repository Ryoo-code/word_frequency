from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #http://127.0.0.1:8000/のURLにアクセスした際に、analyzer内のurls.pyを読み込んで処理
    path('', include('analyzer.urls'))
]