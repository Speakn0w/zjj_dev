import asyncio
import sys
import random
from volcenginesdkarkruntime import AsyncArk
from datetime import datetime, timedelta
sys.path.append('/home/ittc819/zjj/gpt4')
from lunar import Lunar
from datetime import datetime

# Authentication
# 1.If you authorize your endpoint using an API key, you can set your api key to environment variable "ARK_API_KEY"
# or specify api key by Ark(api_key="${YOUR_API_KEY}").
# Note: If you use an API key, this API key will not be refreshed.
# To prevent the API from expiring and failing after some time, choose an API key with no expiration date.

# 2.If you authorize your endpoint with Volcengine Identity and Access Management（IAM), set your api key to environment variable "VOLC_ACCESSKEY", "VOLC_SECRETKEY"
# or specify ak&sk by Ark(ak="${YOUR_AK}", sk="${YOUR_SK}").
# To get your ak&sk, please refer to this document(https://www.volcengine.com/docs/6291/65568)
# For more information，please check this document（https://www.volcengine.com/docs/82379/1263279）
client = AsyncArk(api_key="0b875849-8365-495f-acfa-3837842c4ba0")

mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Sex dictionary for random selection
sex_dict = {
    0: "女性",
    1: "男性"
}

def generate_random_birthdate():
    # Generate a random birthdate within a range
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2000, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

async def main():
     for _ in range(10):  # Loop to create 10 test cases
        print("begin")
        print("###########################")
        birthdate = generate_random_birthdate()
        sex = random.randint(0, 1)
        mbti = random.choice(mbti_types)
        print(f"Testing for Birthdate: {birthdate}, Sex: {sex_dict[sex]}, MBTI: {mbti}")

        # Constructing the test case payload
        year = birthdate.year
        month = birthdate.month
        day = birthdate.day
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
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

        new_eightchar_dict = {
            "生日": f"{year}年{month}月{day}日{hour}时{minute}分",
            "八字": eightchar_dic["八字"],
            "性别": eightchar_dic["性别"],
            "纳音": eightchar_dic["纳音"],
            "MBTI": mbti,
        }

        sys_prompt = "你现在是一位周易八卦学的专家，神秘学大师，珠宝领域的专家，遇到任何问题或会话请求时，都请你按照要求的应答方式进行回答:\
            前置知识:\
            #############\
            基于输入的MBTI和性别，查询预设宝石对应表：\
            - 如果MBTI为 INTJ, INTP, ENTJ, ENTP:\
            - 男: 返回宝石 '堇青石'\
            - 女: 返回宝石 '紫珍珠'\
            - 如果MBTI为 INFJ, INFP, ENFJ, ENFP:\
            - E: 返回宝石 '祖母绿'\
            - I: 返回宝石 '翡翠'\
            - 如果MBTI为 ISTJ, ISFJ, ESTJ, ESFJ:\
            - T: 返回宝石 '海蓝石'\
            - F: 返回宝石 '绿松石'\
            - 如果MBTI为 ISTP, ISFP, ESTP, ESFP:\
            - T: 返回宝石 '黄水晶'\
            - F: 返回宝石 '琥珀'\
            #############\
            宝石对应的三种关键词如下:\
            1.堇青石: 智慧 ## 清晰 ## 忠诚\
            2.紫珍珠: 智慧 ## 共鸣 ## 平衡\
            3.海蓝石: 洞察 ## 慈悲 ## 创造\
            4.绿松石: 理想 ## 和平 ## 慈悲\
            5.金红石: 力量 ## 乐观 ## 变革\
            6.琥珀: 活力 ## 探索 ## 灵活\
            7.祖母绿: 成长 ## 承诺 ## 坚韧\
            8.翡翠: 平衡 ## 责任 ## 守护\
            #############\
            用户输入如下:\
            八字: [用户的八字]\
            性别: [用户的性别]\
            纳音: [用户的纳音]\
            MBTI: [用户的MBTI类型]\
            #########################\
            请按照如下的要求进行回答:\
            1.请使用文言文结合白话文回答,并且说话含蓄内敛，不要回答的太直接\
            2.回答的长度长一些，分析的详细一些，不要重复用户的问题\
            3.尽量将话题向积极向上的方向引导\
            4.说话语言尽量亲切、温和一些\
            5.你善于根据用户输入的八字、纳音五行和性别信息，以及根据你深入掌握的命理、五行、八字专业知识，\
            进行五行、八字命理方面深入分析、洞察这五行、八字命理所蕴含的命理特征，及预测我的事业、婚姻、财运、学业、健康、子女等方面的情况，输出深入洞察的分析结果\
            6.请深入理解并学习易经内容,并融会贯通，深入掌握中国古代命理八字算命技术，并参考至少一句以上的原文进行回答\
            ##################\
            回答格式:\
            从宝石关键词对应表中获取三个关键词及其解释：\
            - 根据宝石名称，查找对应的三个关键词。\
            - 结合用户的八字和纳音，生成每个关键词的50-100字解释。\
                生成输出：\
                宝石: [选定的宝石]\
                关键词1: [关键词1] - 解释: [结合八字和纳音的解释]\
                关键词2: [关键词2] - 解释: [结合八字和纳音的解释]\
                关键词3: [关键词3] - 解释: [结合八字和纳音的解释]"
        stream = await client.chat.completions.create(
        model="ep-20240726181421-rfxtl",
        messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"{new_eightchar_dict}"},
            ],
            stream=True
        )
        async for completion in stream:
            print(completion.choices[0].delta.content, end="")
        print("end")
        print("###########################")

if __name__ == "__main__":
    asyncio.run(main())