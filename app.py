from flask import Flask
from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from utils import AbsUtils
import requests

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

@app.route('/jslpa', methods=['GET', 'POST'])
def js_get_list():
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "http://www.jslpa.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.jslpa.cn/UserView/CourseList",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cookies = {
        "xn_dvid_kf_20023": "E9BCBE-F2F3CE99-17A7-1EA8-B3E9-08A6CBC85A18",
        "p_h5_u": "613B487A-98E8-4B2B-998B-6C04AC4987EB",
        "xn_sid_kf_20023": "1714954135532125",
        "SECKEY_ABVK": "MlSLrpCwVzgwYsaNNYnBd6iTzPzCTK/OpwyLLnYK2wM%3D",
        "ASP.NET_SessionId": "ddkeqtb3zdsh0dxoj44vofe3",
        "BMAP_SECKEY": "MlSLrpCwVzgwYsaNNYnBd41Yg2exYhKUUtkh4Nz-DWFjHZu5zuuZtOHlwiXYy3DECfpMU-PuUSdPQZ31qw1K7bEu6ZPxSHK9p0nHoFRWrGIywRn9M8LfERwRg6xmcazXbkrgGIF9MIrck5J-iWd-ZUY9eiOaY8VKm2SMFmkuR8AcKoDYVKQPYYUtL_yPcSzq"
    }
    url = "http://www.jslpa.cn/api/Course/List"
    response = requests.post(url, headers=headers, cookies=cookies, verify=False)
    res = "Error"
    if response:
        res = response.json()
    return res

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
