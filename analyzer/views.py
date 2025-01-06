from django.shortcuts import render
from django.views.generic import TemplateView
from collections import Counter #Python標準ライブラリの Counter を使って、リスト内の要素（単語）の頻度を簡単にカウン
import spacy
import os
import pandas as pd
import openai
from django.contrib.auth.decorators import login_required  # 認証デコレーターをインポート
from django.shortcuts import redirect

#英語モデルをダウンロード
nlp = spacy.load("en_core_web_sm")

# ストップワードファイルのパス(親ディレクトリにあるtextファイルとこのファイルをつなぐ)
STOPWORDS_PATH = os.path.join(os.path.dirname(__file__), '..', 'stopwords_up_to_A1.txt')

# ストップワードを読み込む関数（再利用性の為に作成）
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)

# ストップワードリストをロード
custom_stopwords = load_stopwords(STOPWORDS_PATH)

# OpenAI API キーの設定
openai.api_key=""

def generate_sentence(word):
    """ChatGPT API を使用して簡単な英文と和訳を生成する関数"""
    prompt = f"""
    Write a simple English sentence using the word '{word}' with a maximum of 7 words.
    Provide the Japanese translation of that sentence.
    Output should strictly follow this format:
    English: <sentence>
    Japanese: <translation>
    """
    try:
        # 最新API仕様に基づくリクエスト
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}, #systemは性格付け
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )

        # 最新のレスポンス
        reply = response.choices[0].message.content

        # 応答を安全に分割して処理
        lines = reply.split('\n')  # 全行を取得
        sentence = next((line.replace("English:", "").strip() for line in lines if line.startswith("English:")), "No sentence generated.")
        translation = next((line.replace("Japanese:", "").strip() for line in lines if line.startswith("Japanese:")), "No translation available.")

        return sentence, translation
    except Exception as e:
    # 詳細なエラー情報をログ出力
     print(f"API Error: {str(e)}")
     return "Error generating sentence.", f"APIエラー: {str(e)}"

@login_required  # ← 認証必須を追加
def upload(request):
    # http://127.0.0.1:8000/ で表示されるページ
    return render(request, 'analyzer/upload.html')

@login_required
def result(request):
    if request.method == 'POST':
        input_text = request.POST.get('name', '').strip()
        request.session['input_text'] = input_text  # セッションにデータ保存
        return redirect('result')

    # GETリクエスト時はセッションデータを使う
    input_text = request.session.get('input_text', '')
    if input_text:
        doc = nlp(input_text)
        filtered_words = [
            token.lemma_ for token in doc
            if not token.is_stop and token.is_alpha and not token.is_punct
            and token.lemma_.lower() not in custom_stopwords
        ]

        word_count = dict(Counter(filtered_words))
        word_count = {key: value for key, value in word_count.items() if key != "items"}
        df = pd.DataFrame(list(word_count.items()), columns=['Word', 'Frequency'])
        df = df.sort_values(by='Frequency', ascending=False)

        top_words = df.head(10)
        results = []
        for index, row in top_words.iterrows():
            word = row['Word']
            frequency = row['Frequency']
            sentence, translation = generate_sentence(word)
            results.append({'Word': word, 'Frequency': frequency, 'EasySentence': sentence, 'Translation': translation})
        result_df = pd.DataFrame(results)

        result_data = result_df.to_dict(orient='records')

        return render(request, 'analyzer/result.html', {
            'input_text': input_text,
            'word_count': result_data
        })
    else:
        return redirect('upload')  # セッションがなければuploadにリダイレクト