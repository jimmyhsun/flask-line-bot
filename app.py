from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import os
from urllib import parse
import mysql.connector


app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

car={"甜不辣":"30元","米血糕":"40元"}
acc=[]
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
line_login_id = config.get('line-bot', 'line_login_id')
line_login_secret = config.get('line-bot', 'line_login_secret')
my_phone = config.get('line-bot', 'my_phone')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]

                if text == "菜單":
                    payload["messages"] = [getNameEmojiMessage()]
                elif text == "購物車":
                    payload["messages"] = [getPlayStickerMessage()]
                elif text == "台北101圖":
                    payload["messages"] = [getTaipei101ImageMessage()]
                elif text == "台北101影片":
                    payload["messages"] = [getMRTVideoMessage()]
                elif text == "台北101":
                    payload["messages"] = [getTaipei101ImageMessage(),
                                            getTaipei101LocationMessage(),
                                            getMRTVideoMessage()]
                elif text == "消費紀錄查詢":
                    payload["messages"] = [getspend()]
                elif text == "食物":
                    payload["messages"] = [getfood()]
                elif text == "主選單":
                    payload["messages"] = [
                            {
                                "type": "template",
                                "altText": "This is a buttons template",
                                "template": {
                                  "type": "buttons",
                                  "title": "Menu",
                                  "text": "Please select",
                                  "actions": [
                                      {
                                        "type": "message",
                                        "label": "我的名字",
                                        "text": "我的名字"
                                      },
                                      {
                                        "type": "message",
                                        "label": "今日確診人數",
                                        "text": "今日確診人數"
                                      },
                                      {
                                        "type": "uri",
                                        "label": "聯絡我",
                                        "uri": f"tel:{my_phone}"
                                      }
                                  ]
                              }
                            }
                        ]
                else:
                    payload["messages"] = [
                            {
                                "type": "text",
                                "text": text
                            }
                        ]
                replyMessage(payload)
            elif events[0]["postback"]["data"] == "30元":
                 car_one.append(30)

        elif events[0]["type"] == "postback":
            if "params" in events[0]["postback"]:
                reservedTime = events[0]["postback"]["params"]["datetime"].replace("T", " ")
                payload["messages"] = [
                        {
                            "type": "text",
                            "text": F"已完成預約於{reservedTime}的叫車服務"
                        }
                    ]
                replyMessage(payload)
            elif events[0]["postback"]["data"] == "30元":
                 acc.append(("甜不辣",30))
                
            elif events[0]["postback"]["data"] == "40元":
                 acc.append(("米血糕",40))
                 
            else:
                data = json.loads(events[0]["postback"]["data"])
                action = data["action"]
                if action == "get_near":
                    data["action"] = "get_detail"
                    payload["messages"] = [getCarouselMessage(data)]
                elif action == "get_detail":
                    del data["action"]
                    payload["messages"] = [getTaipei101ImageMessage(),
                                           getTaipei101LocationMessage(),
                                           getMRTVideoMessage(),
                                           getCallCarMessage(data)]
                replyMessage(payload)

    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
        )


@app.route("/sendTextMessageToMe", methods=['POST'])
def sendTextMessageToMe():
    pushMessage({})
    return 'OK'


def getNameEmojiMessage():
    # message={"type": "flex","altText": "Flex Message","contents":{"type":"carousel","contents":[one]}}
    one={"type": "bubble",
         "hero": {"type": "image",
                        "url": "https://student04.herokuapp.com/static/quality.jpg",
                        "size": "full", "aspectRatio": "20:13","aspectMode": "cover"},
          "body": {"type": "box","layout": "vertical","spacing": "md",
                   "contents": [{"type": "text",
                                "text": "甜不辣",
                                "size": "3xl",
                                "weight": "bold"},
                                {"type": "box","layout": "vertical","spacing": "sm",
                                     "contents": [{"type": "box",
                                                    "layout": "baseline",
                                                    "contents": [{"type": "text","text": "價錢",
                                                                  "weight": "bold",
                                                                   "margin": "sm",
                                                                   "flex": 0,
                                                                   "size": "lg"},
                                                                  {"type": "text",
                                                                    "text": "30元",
                                                                    "size": "lg",
                                                                    "align": "end",
                                                                    "color": "#aaaaaa"}]},
                                                   {"type": "box","layout": "baseline",
                                                    "contents": [{"type": "text","text": "熱量","weight": "bold","margin": "sm","flex": 0,"size": "lg"},
                          {"type": "text",
                            "text": "550kcl",
                            "size": "lg",
                            "align": "end",
                            "color": "#aaaaaa"
                          }]}]}]}}

    two={"type": "bubble",
         "hero": {"type": "image",
                        "url": "https://student04.herokuapp.com/static/quality.jpg",
                        "size": "full", "aspectRatio": "20:13","aspectMode": "cover"},
          "body": {"type": "box","layout": "vertical","spacing": "md",
                   "contents": [{"type": "text",
                                "text": "米血糕",
                                "size": "3xl",
                                "weight": "bold"},
                                {"type": "box","layout": "vertical","spacing": "sm",
                                 "contents": [{"type": "box",
                                                    "layout": "baseline",
                                                    "contents": [{"type": "text","text": "價錢",
                                                                  "weight": "bold",
                                                                   "margin": "sm",
                                                                   "flex": 0,
                                                                   "size": "lg"},
                                                                  {"type": "text",
                                                                    "text": "40元",
                                                                    "size": "lg",
                                                                    "align": "end",
                                                                    "color": "#aaaaaa"}]},
                                                   {"type": "box","layout": "baseline",
                                                    "contents": [{"type": "text","text": "熱量","weight": "bold","margin": "sm","flex": 0,"size": "lg"},
                          {"type": "text",
                            "text": "560kcl",
                            "size": "lg",
                            "align": "end",
                            "color": "#aaaaaa"
                          }]}]}]}}

    message = {"type": "flex", "altText": "Flex Message", "contents": {"type": "carousel", "contents": [one,two]}}
             
    return message

def getCarouselMessage(data):
    message = {
          "type": "template",
          "altText": "this is a image carousel template",
          "template": {
              "type": "image_carousel",
              "columns": [
                  {
                    "imageUrl": F"{end_point}/static/taipei_101.jpeg",
                    "action": {
                      "type": "postback",
                      "label": "台北101",
                      "data": json.dumps(data)
                    }
                  },
                  {
                    "imageUrl": F"{end_point}/static/taipei_1.jpeg",
                    "action": {
                      "type": "postback",
                      "label": "台北101",
                      "data": json.dumps(data)
                    }
                  }
                  # {
                  #   "imageUrl": "https://example.com/bot/images/item3.jpg",
                  #   "action": {
                  #     "type": "uri",
                  #     "label": "View detail",
                  #     "uri": "http://example.com/page/222"
                  #   }
                  # }
              ]
          }
        }
    return message


def getLocationConfirmMessage(title, latitude, longitude):
    data = {"title":title , "latitude":latitude , "longitude":longitude , "action":"get_near"}
    message = {"type": "template",
                "altText": "this is a confirm template",
                "template": {
                    "type": "confirm",
                    "text": f"確認是否搜尋{title}附近地點？",
                    "actions": [{"type": "postback",
                                "label": "是",
                                "data": json.dumps(data)},
                                {"type": "message", "label": "否", "text": "否"}]
                        }
              }
    return message


def getCallCarMessage(data):
    message = {"type": "template",
                "altText": "this is a confirm template",
                "template": {
                    "type": "buttons",
                    "text": f"請選擇是否{data['title']}預約叫車時間",
                    "actions": [{"type": "datetimepicker",
                                "label": "預約",
                                "data": json.dumps(data),
                                "mode":"datetime"}
                                ]
                        }
              }
    return message


def getPlayStickerMessage():
    a=sorted(acc,key=lambda acc:acc[1])
    message = {"type": "text", "text":f"你所點的項目{a}"}
    return message


def getTaipei101LocationMessage():
    message = dict()
    message["type"] = "location"
    message["title"] ="Taipei 101"
    message["address"] ="台北市信義路五段7號"
    message["latitude"] =25.034056468449304
    message["longitude"] =121.56466736984362
    return message


def getMRTVideoMessage():
    message = dict()
    message ["type"]="video"
    message["originalContentUrl"] = F"{end_point}/static/taipei_101_video.mp4"
    message["previewImageUrl"] = F"{end_point}/static/taipei_101.jpeg"
    return message


def getMRTSoundMessage():
    message = dict()
    message["type"] = "audio"
    message["originalContentUrl"] = F"{end_point}/static/mrt_sound.m4a"
    import audioread
    with audioread.audio_open('static/mrt_sound.m4a') as f:
        # totalsec contains the length in float
        totalsec = f.duration
    message["duration"] = totalsec * 1000
    return message


def getTaipei101ImageMessage(originalContentUrl=F"{end_point}/static/taipei_101.jpeg"):
    return getImageMessage(originalContentUrl)


def getImageMessage(originalContentUrl):
    message = dict()
    message ["type"]="image"
    message["originalContentUrl"] = originalContentUrl
    message["previewImageUrl"] = originalContentUrl
    return message


def replyMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/reply",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def pushMessage(payload):
    response = requests.post("https://api.line.me/v2/bot/message/push",headers=HEADER,data=json.dumps(payload))
    return 'OK'


def getspend():
    connection = mysql.connector.connect(host="35.221.178.251",
                                         database="project",
                                         user="root",
                                         password="cfi10202")
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM details where userid=001")
    myresult = mycursor.fetchall()
    showlist = "".join(f"{x[3]} 數量 {x[4]}" for x in myresult)

    messages = {"type": "text", "text": f"{showlist}"}
    return messages


def getfood():
    connection = mysql.connector.connect(host="35.221.178.251",
                                        database="project",
                                        user="root",
                                        password="cfi10202")
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM products")
    myresult = mycursor.fetchall()
    showlist = "".join(f"{x[1].ljust(30, '-')}{str(x[2]).rjust(4)}元 ({x[2]}大卡)\n" for x in myresult)
    
    messages={"type":"text","text":f"{showlist}"}

    return messages


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
def upload_file():
    payload = dict()
    if request.method == 'POST':
        file = request.files['file']
        print("json:", request.json)
        form = request.form
        age = form['age']
        gender = ("男" if form['gender'] == "M" else "女") + "性"
        if file:
            filename = file.filename
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)
            print(img_path)
            payload["to"] = my_line_id
            payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
                {
                    "type": "text",
                    "text": F"年紀：{age}\n性別：{gender}"
                }
            ]
            pushMessage(payload)
    return 'OK'


@app.route('/line_login', methods=['GET'])
def line_login():
    if request.method == 'GET':
        code = request.args.get("code", None)
        state = request.args.get("state", None)

        if code and state:
            HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = "https://api.line.me/oauth2/v2.1/token"
            FormData = {"grant_type": 'authorization_code', "code": code, "redirect_uri": F"{end_point}/line_login", "client_id": line_login_id, "client_secret":line_login_secret}
            data = parse.urlencode(FormData)
            content = requests.post(url=url, headers=HEADERS, data=data).text
            content = json.loads(content)
            url = "https://api.line.me/v2/profile"
            HEADERS = {'Authorization': content["token_type"]+" "+content["access_token"]}
            content = requests.get(url=url, headers=HEADERS).text
            content = json.loads(content)
            name = content["displayName"]
            userID = content["userId"]
            pictureURL = content["pictureUrl"]
            statusMessage = content["statusMessage"]
            print(content)
            connection = mysql.connector.connect(host="35.221.178.251",
                                                 database="project",
                                                 user="root",
                                                 password="cfi10202")
            mycursor = connection.cursor()
            command = "insert into users(userid, user_name) values('{:s}','{:s}');".format(userID, name)
            mycursor.execute(command)
            connection.commit()
            return render_template('profile.html', name=name, pictureURL=
                                   pictureURL, userID=userID, statusMessage=
                                   statusMessage)
        else:
            return render_template('login.html', client_id=line_login_id,
                                   end_point=end_point)

@app.route('/shoppingcar', methods=['GET'])
def shoppingcar():
    return render_template(r"try.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
