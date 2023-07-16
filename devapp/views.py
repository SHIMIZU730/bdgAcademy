import os
import time
import io
from datetime import date, datetime
import logging
import imghdr
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
import tempfile
import base64
from django.contrib import messages
import boto3
from base64 import b64decode
import openai
import stat
from django.core.files.storage import default_storage
from django.views.generic import TemplateView
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
from common.const import *
from .models import chatgpt_answer_log
from pathlib import Path
from django.core.files.base import ContentFile
from django.utils import timezone

logger = logging.getLogger('django')
    
# ===================================================
# 初期画面を表示
# ===================================================
class IndexTemplateView(TemplateView):
    template_name = "index.html"

class detectBoardgame(generic.View):
    
    def get(self, request, *args, **kwargs):    
        
        template_name = 'detecrBdg.html'
        
        context = {
            'gptResultList': None,
            'image_url': None,
            'bg_result': 'images/bg-result.jpg',
            'bg_search': 'images/bg-search.jpg',
        }
        
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        
        image_url = None
        gptResultList =[]

        # ボードゲーム情報取得
        if 'searchBdg' in request.POST:
            
            # 利用回数をチェックする
            if checkUseCnt(request):
                messages.error(request, useCntOver_errText)
            else:
                if 'inputImg' in request.FILES:
                    
                    uploadedFile = request.FILES['inputImg']
                    
                    # 画像かどうかチェック
                    result = is_image(uploadedFile)
                    
                    if result == False:
                        messages.error(request, notImageFile_errText)
                    else:
                        # mediaフォルダ内の画像が一定量超えたら削除
                        delete_old_images()
                        
                        # アップロードした画像を画面に表示する
                        image_url = displayDetectedImage(uploadedFile)
                        
                        # 画像からChatGPT起動
                        gptResultList = searchBdgByImage(uploadedFile)
                    
        elif 'searchBdgByText' in request.POST:
            if request.POST.get('inputText') != '':
                # 利用回数をチェックする
                if checkUseCnt(request):
                    messages.error(request, useCntOver_errText)
                else:
                    # テキストからChatGPT起動
                    gptResultList = searchBdgByText(request)
            # else:
                # messages.error(request, bdgBlank_errText)
                
            
        template_name = 'detecrBdg.html'
        
        context = {
            'gptResultList': gptResultList,
            'image_url': image_url,
            'bg_result': 'images/bg-result.jpg',
            'bg_search': 'images/bg-search.jpg',
        }
        return render(request, template_name, context)
        
        
# ===================================================
# 画像からボードゲーム情報を取得
# ===================================================
def searchBdgByImage(file):
    
    gptResultList = []
    img = None
    
    REGION_NAME = os.environ.get('REGION_NAME')
    
    # # 画像リサイズテスト用コード
    # # アップロードファイルの画像ファイルテスト確認用
    # size_in_mb = file.size / (1024 * 1024)
    # # 画像ファイルのサイズを取得（バイト単位）
    # print(f"アップロード画像のファイルサイズ: {size_in_mb} MB")

    if file.size > 5242880:  # 5MB以上ならリサイズ
        base_width = 1000
        img = resize_image(file,base_width)
    else:
        img = Image.open(file)
        
    # # 画像リサイズテスト用コード
    # # 画像リサイズ後に一時的なファイルに保存
    # temp_img_file = tempfile.NamedTemporaryFile(delete=True)
    # img.save(temp_img_file.name, 'JPEG')
    # # 圧縮後の画像ファイルサイズを取得
    # size_in_mb_after = os.path.getsize(temp_img_file.name) / (1024 * 1024)
    # print(f"圧縮後のファイルサイズ: {size_in_mb_after:.2f} MB")

    # 画像をBytesに変換
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Rekognition clientの作成
    reko = boto3.client('rekognition', region_name=REGION_NAME)
    
    # AWS rekognitionの実行
    response = reko.detect_text(
        Image={
            'Bytes': img_byte_arr
        }
    )

    # 抽出したデータをカンマ区切りのデータに変換
    extracted_textsStr = ''
    for text_detection in response['TextDetections']:
        if extracted_textsStr != '':
            extracted_textsStr += ','
        extracted_textsStr += text_detection['DetectedText']
    
    # プロンプト生成    
    prompt = generatePrompt(extracted_textsStr)
    
    # ChatGPT起動
    gptResultList = startChatGpt(prompt)

    return gptResultList

# ===================================================
# セットされる画像ファイルが画像かどうかを判定
# ===================================================
def is_image(file):
    # imghdr.what()はファイルのタイプを返します。画像でない場合はNoneを返します。
    img_type = imghdr.what(file)
    return img_type is not None


# ===================================================
# 画像をリサイズする
# ===================================================
def resize_image(file, base_width):
    img = Image.open(file)

    # 画像の元の幅と高さを取得
    w_orig, h_orig = img.size

    # 新しい高さを計算（アスペクト比を保つ）
    new_height = base_width * h_orig / w_orig

    # リサイズ
    img = img.resize((base_width, int(new_height)), Image.ANTIALIAS)
    return img

# ===================================================
# テキスト入力からボードゲーム情報を取得
# ===================================================
def searchBdgByText(request):
    
    text_data = request.POST['inputText']
    
    # プロンプト生成
    prompt = generatePrompt(text_data)

    # ChatGPT起動
    gptResultList = startChatGpt(prompt)
    
    return gptResultList
  
    
# ===================================================
# ChatGPT起動 引数：質問内容
# ===================================================
def startChatGpt(prompt):
    
    gptResultList = []
    
    openai.api_key = os.environ.get('OPENAI_APIKEY')
    
    messages = [
      # ChatGPTとの対話内容：
      # {"role": ロール, "content": メッセージ}という辞書を要素とするリスト
      {"role": "user", "content": prompt}
    ]
    
    completion = None
    
    for i in range(max_retries):
        try:
            # OpenAI APIの呼び出し
            completion = openai.ChatCompletion.create(
              model=gptModel,  # ChatGPT APIを使用するには'gpt-3.5-turbo'などを指定
              messages=messages
            )
            break  # 成功した場合、ループから抜け出す

        except openai.error.APIError as e:
            if '502' in str(e):  # HTTP 502エラーの場合だけ再試行します
                logger.error(f"OpenAIのAPIで502 error発生: {e}. Retry {i+1}/{max_retries} will start after {delay} seconds.")
                time.sleep(delay)  # 指定した秒数だけ待ちます
            else:
                logger.error(f"OpenAIのAPIでAPIエラー発生: {e}")
                raise  # 502エラー以外は例外をそのまま投げます

        except openai.error.APIConnectionError as e:
            # 接続エラーの取り扱い
            logger.error(f"OpenAIのAPI接続エラー: {e}")
            raise  # 例外をそのまま投げます

        except openai.error.RateLimitError as e:
            # レート制限エラーの取り扱い（指数バックオフを推奨）
            logger.error(f"OpenAIのAPI requestレート制限エラー: {e}")
            raise  # 例外をそのまま投げます
        
    if completion is None:
        raise Exception("ChatGPTでエラーが発生しました。")  # 最大試行回数を超えた場合、エラーを投げます
    
    # ChatGPTからの回答の1つ目を取得し、改行コードを区切りとして分割する。
    gptResult = completion.choices[0].message.content
    gptResultList = gptResult.split('\n')
    
    logger.info("ChatGPT回答1 : " + gptResultList[0])
    
    # DBに回答を保存
    if gptResultList:
        InsertChatGptAnsLog(gptResultList)

    count = 1
    listNo = count -1
    for result in gptResultList:
        if result[0:2] == str(count) + ".":
            gptResultList[count-1] = result[2:]
        count += 1

    return gptResultList

# ===================================================
# プロンプト生成
# ===================================================
def generatePrompt(inputBdgNmText):
    
    prompt = ""
    prompt += chatgpt_jouken
    prompt += kaiGyou
    prompt += chatgpt_quwstion1
    prompt += kaiGyou
    prompt += inputBdgNmText
    prompt += kaiGyou
    prompt += chatgpt_quwstion2
    prompt += kaiGyou
    prompt += chatgpt_quwstion3
    prompt += kaiGyou
    prompt += chatgpt_quwstion4
    prompt += kaiGyou
    prompt += chatgpt_quwstion5
    
    return prompt
    
    
# ===================================================
# mediaフォルダ内の���像を一定数超えたら削除する
# ===================================================
def delete_old_images():
    # メディアフ��ル��内のファイルのリストを取��します。
    files = os.listdir(settings.MEDIA_ROOT)
    
    # ファイルの数を取得します。
    num_images = len(files)
    
    # 画像ファイルの数が上限を超えている場合
    if num_images > maxImages:
    
        # 古い画像ファイルを削除します。
        for file in files[:num_images - maxImages]:
            os.remove(os.path.join(settings.MEDIA_ROOT, file))
            
# ===================================================
# アップロードした画像を画面に表示する
# ===================================================
def displayDetectedImage(file):
    # 画像を画面に表示するため
    file_name = default_storage.save(file.name, file)
    image_url = default_storage.url(file_name)
    
    # ファイルのパーミッションを取得
    uploadedImage = os.path.join(settings.MEDIA_ROOT, file_name)
    file_stat = os.stat(uploadedImage)
    current_permissions = stat.S_IMODE(file_stat.st_mode)
    
    # パーミッションが「-rw-------」（0o600）であれば、パーミッションを変更
    if current_permissions == 0o600:
        # ファイルのパーミッション�������変更（所有者：読み書き、他のユーザー：読み取り）
        os.chmod(uploadedImage, 0o644)
        
    return image_url
    
            
# ===================================================
# ChatGPTの回答をDBに保存
# ===================================================
def InsertChatGptAnsLog(gptResultList):
    try:
        answer_list = [''] * 15
        for i, result in enumerate(gptResultList):
            if result != '':
                answer_list[i] = result
                
        new_data = chatgpt_answer_log(
            answer_1=answer_list[0],
            answer_2=answer_list[1],
            answer_3=answer_list[2],
            answer_4=answer_list[3],
            answer_5=answer_list[4],
            answer_6=answer_list[5],
            answer_7=answer_list[6],
            answer_8=answer_list[7],
            answer_9=answer_list[8],
            answer_10=answer_list[9],
            answer_11=answer_list[10],
            answer_12=answer_list[11],
            answer_13=answer_list[12],
            answer_14=answer_list[13],
            answer_15=answer_list[14],
            create_user='anonymous',
            create_date=timezone.now()
        )
        new_data.save()
    
    except Exception as e:
        logger.error(e)
        
        
# ===================================================
# 利用回数をチェック(日にちが変わればリセットする)
# ===================================================
def checkUseCnt(request):
    
    returnVal = False
    
    # セッションに'click_count'や'click_date'がなければ、初期値を設定します。
    if not 'click_count' in request.session or not 'click_date' in request.session:
        request.session['click_count'] = 0
        request.session['click_date'] = date.today().isoformat()
    
    # セッションから'click_count'と'click_date'を取得します。
    click_count = request.session['click_count']
    click_date = date.fromisoformat(request.session['click_date'])
        
    # クリック日が今日の日付と異なる場合（新たな日になった場合）、カウントと日付をリセットします。
    if click_date != date.today():
        click_count = 0
        click_date = date.today()
    
    # クリック回数が特定の制限を超えていないか確認します。
    if click_count >= maxUseCnt:
        returnVal = True
    
    # クリック回数とクリック日を更新します。
    request.session['click_count'] = click_count + 1
    request.session['click_date'] = click_date.isoformat()
    
    return returnVal