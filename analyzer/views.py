from django.shortcuts import render
from django.views.generic import TemplateView
from collections import Counter #Python標準ライブラリの Counter を使って、リスト内の要素（単語）の頻度を簡単にカウン

def upload(request):
    # http://127.0.0.1:8000/ で表示されるページ
    return render(request, 'analyzer/upload.html')

def result(request):
    if request.method == 'POST':  # POSTリクエストの場合
        input_text = request.POST.get('name', '').strip()  # フォームデータを取得、空白を除去     
        # --- 単語の分割と頻度カウント ---
        words = input_text.split()  # テキストをスペースで分割
        word_count = dict(Counter(words)) # 単語の頻度をカウント,result.htmlの.items()は辞書型のみ有効
        
        # 結果をテンプレートに渡す
        return render(request, 'analyzer/result.html', {
            'input_text': input_text,
            'word_count': word_count
        })
    else:
        # GETリクエストの場合(ユーザーがブラウザで直接/result/にアクセスした時)
        return render(request, 'analyzer/result.html', {
            'input_text': '',
            'word_count': {}
        })