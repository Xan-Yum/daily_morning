from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
today1 = datetime.now().strftime('%Y-%m-%d')

city = os.environ['CITY']
city1 = os.environ['CITY1']
birthday = os.environ['BIRTHDAY']
birthday1 = os.environ['BIRTHDAY1']
start_date = os.environ['START_DATE']
exam_date = os.environ['EXAM_DATE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    url1 = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
    res = requests.get(url).json()
    res1 = requests.get(url1).json()
    weather = res['data']['list'][0]
    weather1 = res1['data']['list'][0]
    return weather['city'], weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low']),\
           weather1['city'], weather1['weather'], math.floor(weather1['temp']), math.floor(weather1['high']), math.floor(weather1['low'])


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_exam_count():
    exam_date = datetime.strptime(exam_date, "%Y-%m-%d") - today
    return exam_date.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_birthday1():
    next = datetime.strptime(str(date.today().year) + "-" + birthday1, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
ci, wea, temperature, highest, lowest, ci1, wea1, temperature1, highest1, lowest1 = get_weather()
data = {"date": {"value": today1, "color": get_random_color()},
        "city": {"value": ci, "color": get_random_color()},
        "weather": {"value": wea,"color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "highest": {"value": highest, "color": get_random_color()},
        "lowest": {"value": lowest, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "city1": {"value": ci1, "color": get_random_color()},
        "weather1": {"value": wea, "color": get_random_color()},
        "temperature1": {"value": temperature, "color": get_random_color()},
        "highest1": {"value": highest, "color": get_random_color()},
        "lowest1": {"value": lowest, "color": get_random_color()},
        "exam_date": {"value": get_exam_count(), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(), "color": get_random_color()},
        "birthday_left1": {"value": get_birthday1(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}}

count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count += 1

print("发送了" + str(count) + "条消息")
