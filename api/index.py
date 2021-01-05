import os
from flask import Flask, request
import functions.elepoke as elepoke
from flask_cors import CORS


# Flaskのセットアップ
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)


@app.route("/", methods=['GET'])
def show():
    return "HELLO ELEPOKE!!"


@app.route("/fit", methods=['POST'])
def getData():
    # POST通信で送られたデータを取得
    _POST = request.get_json()

    # 送信用のデータを格納するための配列
    mypokeList = []
    oppokeList = []

    for mypoke in _POST['mypoke']:
        mypokeList.append(mypoke)

    for oppoke in _POST['oppoke']:
        oppokeList.append(oppoke)

    # 学習
    el = elepoke.Elepoke()
    el.append(name=[mypokeList, oppokeList], reset=True)
    el.fit()

    # 結果を整形
    result = el.result
    jsonData = {"mypoke": result[0], "oppoke": result[1]}

    return jsonData


if __name__ == '__main__':
    app.run()
