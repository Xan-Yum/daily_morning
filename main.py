from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from borax.calendars.lunardate import LunarDate
import requests
import os
import random

today_solar = datetime.now()
today_lunar = LunarDate.today()
today_solar_str = today_solar.strftime('%Y-%m-%d')
today_lunar_str = today_lunar.cn_month + "月" + today_lunar.cn_day + " 星期" + today_lunar.cn_week
# today1 = today_lunar.cn_year + "年 " + today_lunar.cn_month + "月" + today_lunar.cn_day + " 星期" + today_lunar.cn_week
# week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
# today_str = datetime.now().strftime('%Y-%m-%d') + ' ' + week_list[today.weekday()]

city = os.environ['CITY']
city1 = os.environ['CITY1']
birthday_lunar = os.environ['BIRTHDAY'].split(",")
birthday_solar = os.environ['BIRTHDAY1'].split(",")
province = os.environ['PROVINCE']
province1 = os.environ['PROVINCE1']
start_date = os.environ['START_DATE']
exam_date = os.environ['EXAM_DATE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split(",")
template_id = os.environ["TEMPLATE_ID"]

birthday = []
data = {}


# 获取生日列表
def get_birth_lsit():
    for index, i in enumerate(birthday_lunar):
        birthday.append(i)
    for index, j in enumerate(birthday_solar):
        birthday.append(j)
    return birthday


# 生日农历改阳历
def get_lunar_birth(birth):
    # 为读取农历生日准备
    lubaryear = today_lunar.year
    if len(birth) == 10:
        x = int(birth[0:4:1])  # 读取无用，为理解下面两行留着，可删去
        y = int(birth[5:7])  # 切片
        z = int(birth[8:10])
    elif len(birth) == 5:
        y = int(birth[0:2])  # 切片
        z = int(birth[3:5])
    birth1 = LunarDate(lubaryear, y, z)  # 构建今年农历生日日期
    return birth1.to_solar_date().strftime('%m-%d')  # 转化成公历日期，输出为字符串


# 批量生日农历改阳历
def lunar_birth_list(birth):
    for index, i in enumerate(birth):
        birth[index] = get_lunar_birth(i)
    return birth


# 获取天气数据
def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    url1 = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city1
    res = requests.get(url).json()
    res1 = requests.get(url1).json()
    weather = res['data']['list'][0]
    weather1 = res1['data']['list'][0]
    return weather['city'], weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low']),\
           weather1['city'], weather1['weather'], math.floor(weather1['temp']), math.floor(weather1['high']), math.floor(weather1['low'])


# 获取疫情数据
def get_virus():
    url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf"
    req = requests.get(url)
    req_json = req.json()['data']['diseaseh5Shelf']['areaTree'][0]['children']

    for i in range(1, len(req_json)):
        if req_json[i]['name'] == province:
            # print(req_json[i])
            for j in range(1, len(req_json[i]['children'])):
                if req_json[i]['children'][j]['name'] == city:
                    req_data = req_json[i]['children'][j]['today']
                    # return req_data['local_confirm_add'], req_data['wzz_add']
                    # print(req_json[i]['children'][j]['name'])
        # print(req_json)
    for i in range(1, len(req_json)):
        if req_json[i]['name'] == province1:
            # print(req_json[i])
            for j in range(1, len(req_json[i]['children'])):
                if req_json[i]['children'][j]['name'] == city1:
                    req_data1 = req_json[i]['children'][j]['today']

    return req_data['local_confirm_add'], req_data['wzz_add'], req_data1['local_confirm_add'], req_data1['wzz_add']


# 获取纪念日天数
def get_count():
    delta = today_solar - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 获取倒计时天数
def get_exam_count():
    countdown = datetime.strptime(exam_date, "%Y-%m-%d") - today_solar
    return countdown.days


# 获取生日倒计时天数
def get_birthday(birth):
    if len(birth) == 10:
        birth = birth[5:10]
    next = datetime.strptime(str(date.today().year) + "-" + birth, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today_solar).days


# 批量获取生日倒计时
def birth_countdown_list(birth):
    for index, i in enumerate(birth):
        birth[index] = get_birthday(i)
    return birth


# 获取每日一言
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 自定义菜单
client = WeChatClient(app_id, app_secret)
client.menu.create({
    "button": [
        {
            "type": "view",
            "name": "个人博客",
            "url": "https://waluna.top"
        },
        {
            "type": "view",
            "name": "机器人luna",
            "url": "https://openai.weixin.qq.com/webapp/MUVBpsFPvT1XTXhvn2IbUIdHVF3Jea?robotName=luna"
        },
        {
            "name": "菜单",
            "sub_button": [
                {
                    "type": "view",
                    "name": "搜索",
                    "url": "http://www.baidu.com/"
                },
                {
                    "type": "view",
                    "name": "音乐",
                    "url": "https://music.163.com/playlist?id=7006123960&userid=4991541804"
                },
                {
                    "type": "view",
                    "name": "视频",
                    "url": "http://v.qq.com/"
                },
                {
                    "type": "click",
                    "name": "赞一下我们",
                    "key": "V1001_GOOD"
                }
            ]
        }
    ]
})


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

# 批量生日农历改阳历
birthday_lunar = lunar_birth_list(birthday_lunar)

# 获取生日列表
birthday = get_birth_lsit()

# 获取所有生日倒计时
birth_countdown_list = birth_countdown_list(birthday)

# 获取天气数据
ci, wea, temperature, highest, lowest, ci1, wea1, temperature1, highest1, lowest1 = get_weather()

# 获取疫情数据
local_confirm_add, wzz_add, local_confirm_add1, wzz_add1 = get_virus()

# 所有模板数据
data = {
    "1": {"value": today_solar_str, "color": get_random_color()},
    "2": {"value": today_lunar_str, "color": get_random_color()},
    "3": {"value": ci, "color": get_random_color()},
    "4": {"value": wea, "color": get_random_color()},
    "5": {"value": str(temperature) + "℃", "color": get_random_color()},
    "6": {"value": str(lowest) + "℃ ~ " + str(highest) + "℃", "color": get_random_color()},
    "7": {"value": get_count(), "color": get_random_color()},
    "8": {"value": ci1, "color": get_random_color()},
    "9": {"value": wea1, "color": get_random_color()},
    "a": {"value": str(temperature1) + "℃", "color": get_random_color()},
    "b": {"value": str(lowest1) + "℃ ~ " + str(highest1) + "℃", "color": get_random_color()},
    "c": {"value": get_exam_count(), "color": get_random_color()},
    "d": {"value": get_words(), "color": get_random_color()},
    "f": {"value": local_confirm_add, "color": get_random_color()},
    "g": {"value": wzz_add, "color": get_random_color()},
    "h": {"value": local_confirm_add1, "color": get_random_color()},
    "i": {"value": wzz_add1, "color": get_random_color()}}

for index, i in enumerate(birthday):
    e = "e%d" % index
    data[e] = {
        "value": i,
        "color": get_random_color()
    }

count = 0
for user_id in user_ids:
    res = wm.send_template(user_id, template_id, data, url)
    count += 1

print("发送了" + str(count) + "条消息")
