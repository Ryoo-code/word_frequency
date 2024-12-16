from django.shortcuts import render
from django.views.generic import TemplateView

def home(request):
    #http://127.0.0.1:8000/で表示されるページ
    return render(request, 'templates/analyzer/upload.html')