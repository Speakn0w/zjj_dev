import asyncio
import sys
from volcenginesdkarkruntime import AsyncArk
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

sex_dict = {
    0: "女性",
    1: "男性"
}
baoshi_path = "/home/ittc819/zjj/宝石寓意.txt"
with open(baoshi_path, "r") as f:
    baoshi = f.read()

async def main():
    year = int(input("请输入年份："))
    month = int(input("请输入月份："))
    day = int(input("请输入日期："))
    hour = int(input("请输入小时："))
    minute = int(input("请输入分钟："))
    sex = int(input("请输入性别（0为女性，1为男性）："))
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
        "愿望": "升学顺利",
    }
    sys_prompt = f"你现在是一位周易八卦学的专家，神秘学大师，珠宝领域的专家，遇到任何问题或会话请求时，都请你按照以下的目标和应答方式进行回答:\
         1.请使用文言文结合白话文回答,并且说话含蓄内敛，不要回答的太直接\
         2.回答的长度长一些，分析的详细一些，不要重复用户的问题\
         3.尽量将话题向积极向上的方向引导\
         4.说话语言尽量亲切、温和一些\
         5.你善于根据用户输入的八字、纳音五行和性别信息，以及根据你深入掌握的命理、五行、八字专业知识，\
         进行五行、八字命理方面深入分析、洞察这五行、八字命理所蕴含的命理特征，及预测我的事业、婚姻、财运、学业、健康、子女等方面的情况，输出深入洞察的分析结果\
         6.你可以根据用户提供的（愿望），给出相应的建议，请你的建议具有明确的倾向性，不要模棱两可\
         7.请深入理解并学习易经内容,并融会贯通，深入掌握中国古代命理八字算命技术，并参考至少一句以上的原文进行回答\
         8.深入学习宝石寓意文档的信息，并融会贯通，掌握各个宝石的寓意及其延申，并在宝石文档中选择最符合用户需求的一项，输出在（### title） 里面，宝石文档内容：{baoshi}\
         9.对于用户提出的问题，请你按照如下格式输出回复：\
         ### name\
         ### title\
         ### overall\
         ### wish\
         ### advice \
         10.name（表示用户的姓名）\
         11.title（表示最推荐的宝石,请在宝石文档的内容中进行选择，结合用户的五行、八字、个人信息、愿望进行推荐）\
         12.overall（表示对于用户命理的整体解读，要求结合用户的八字、五行讲解，覆盖的方面广泛一些，结合推荐的宝石讲解，内容丰富一些）\
         13.wish（表示用户的心愿）\
         14.advice（表示针对用户心愿提出的建议，要求详细，具有倾向性）"
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


if __name__ == "__main__":
    asyncio.run(main())