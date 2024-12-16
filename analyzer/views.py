from django.shortcuts import render
from django.views.generic import TemplateView

def upload(request):
    #http://127.0.0.1:8000/で表示されるページ
    return render(request, 'analyzer/upload.html')

def result(request):
    if request.method == 'POST': #フォーム送信時のHTTPリクエストがPOSTメソッドである場合、条件が True 
        input_text = request.POST.get('name') #フォームからデータを取得 .get()メソッドで特定のキーを取得
        # ここで解析処理を実装（仮に入力データをそのまま返す）
        result_data = f"入力された文章:{input_text}"
        return render(request, 'analyzer/result.html',{'result': result_data})
    else:
        return render(request, 'analyzer/result.html',{'result':"データが送信されてません。"}) #第三引数はcontextで、キーと値で構成される辞書