import asyncio
import json
from quart import Quart, request, jsonify
import sys
sys.path.append('/home/ittc819/zjj/gpt4')
from lunar import Lunar
from datetime import datetime

app = Quart(__name__)

sex_dict = {
    0: "女性",
    1: "男性"
}

@app.route('/bazi', methods=['POST'])
async def calculate_bazi():
    data = await request.get_json()
    year = data['year']
    month = data['month']
    day = data['day']
    hour = data['hour']
    minute = data['minute']
    sex = data['sex']

    date = datetime(year, month, day, hour, minute)
    eightchar = Lunar(date)

    eightchar_dic = {
        '农历': '%s %s[%s]年 %s%s' % (eightchar.lunarYearCn, eightchar.year8Char, eightchar.chineseYearZodiac, eightchar.lunarMonthCn, eightchar.lunarDayCn),
        '性别': sex_dict[sex],
        '今日节日': (eightchar.get_legalHolidays(), eightchar.get_otherHolidays(), eightchar.get_otherLunarHolidays()),
        '八字': ' '.join([eightchar.year8Char, eightchar.month8Char, eightchar.day8Char, eightchar.twohour8Char]),
        '今日节气': eightchar.todaySolarTerms,
        '今日时辰': eightchar.twohour8CharList,
        '时辰凶吉': eightchar.get_twohourLuckyList(),
        '生肖冲煞': eightchar.chineseZodiacClash,
        '星座': eightchar.starZodiac,
        '星次': eightchar.todayEastZodiac,
        '彭祖百忌': eightchar.get_pengTaboo(),
        '彭祖百忌精简': eightchar.get_pengTaboo(long=4, delimit='<br>'),
        '十二神': eightchar.get_today12DayOfficer(),
        '廿八宿': eightchar.get_the28Stars(),
        '今日三合': eightchar.zodiacMark3List,
        '今日六合': eightchar.zodiacMark6,
        '今日五行': eightchar.get_today5Elements(),
        '纳音': eightchar.get_nayin(),
        '九宫飞星': eightchar.get_the9FlyStar(),
        '吉神方位': eightchar.get_luckyGodsDirection(),
        '今日胎神': eightchar.get_fetalGod(),
        '神煞宜忌': eightchar.angelDemon,
        '今日吉神': eightchar.goodGodName,
        '今日凶煞': eightchar.badGodName,
        '宜忌等第': eightchar.todayLevelName,
        '宜': eightchar.goodThing,
        '忌': eightchar.badThing,
        '时辰经络': eightchar.meridians
    }

    return jsonify(eightchar_dic)

if __name__ == '__main__':
    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5007"]  # 将绑定地址改为0.0.0.0，允许外部访问
    print("Listening on port 5007")
    
    asyncio.run(hypercorn.asyncio.serve(app, config))