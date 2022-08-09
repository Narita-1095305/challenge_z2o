import requests
import json
import sys
import time

nickname = input("ニックネームを決めてください。")
print(f'nickname:{nickname}')
url = 'http://challenge.z2o.cloud/challenges'

#サーバ側のレスポンスに依存する処理のため、try except文で異常が起きていないか判定
try:
    response_json = (requests.post(url, params={'nickname': nickname})).json()
except:
    print("サーバー側で問題が発生しました。")
    sys.exit(1)
    
isContinue = True
while isContinue:  
    #予定実行時間まで待機。(PC等の実行環境によって待機する時間にラグが生じる。)
    time.sleep((response_json['actives_at'] - response_json['called_at']) * 0.001)
    #サーバ側のレスポンスに依存する処理のため、try except文で異常が起きていないか判定
    try:
        response_json = requests.put(url, headers={'X-Challenge-Id': response_json['id']}).json()
    except:
        print("サーバー側で問題が発生しました。")
        sys.exit(1)
    
    isContinue = False if 'result' in response_json else True

#チャレンジ成功時には「チャレンジ成功」と通知し、URLを表示する。そうでない場合には「チャレンジ失敗」と通知する。
print("チャレンジ失敗…") if response_json['result']['url'] is None else print(f'チャレンジ成功！\nURL:{url.replace("challenges", response_json["result"]["url"])}')

sys.exit(0)