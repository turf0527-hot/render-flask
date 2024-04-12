from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from utils import AbsUtils

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/reContent', methods=['GET', 'POST'])
def re_content():
    if request.method == 'GET':
        return render_template('reContent.html')
    else:
        content_text = request.form.get("content_text")
        # print("接收到的请求:",content_text)
        cont_list = content_text.splitlines()
        # print("接收到的请求:",cont_list)
        result = map(AbsUtils.match_chinese_characters,cont_list)
        res_list = list(result)
        print("处理完的结果:",res_list)
        # return list(result)
        return render_template('reContent.html',data=res_list)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)