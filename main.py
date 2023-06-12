import os
import requests
import asyncio
import telegram
import json
import datetime
from dotenv import load_dotenv


def init():
    load_dotenv()

    global url
    global useStDate
    global helMngerCd
    global useStTime
    global useEdTime
    global userDiv
    global reqEmpNo
    global holidays

    url = "https://talk.tmaxsoft.com/front/health/insertHealth.do?helMngerCd=HEL20220609001"

    helMngerCdMap = {
        "손애화": "HEL20220609001",
        "이승우": "HEL20140101130",
        "정영민": "HEL20210330001",
        "남경인": "HEL20230125001",
    }

    helMnger = os.getenv("helMnger")
    helMngerCd = helMngerCdMap[helMnger]
    useStDate = os.getenv("useStDate")
    useStTime = os.getenv("useStTime")
    useEdTime = useStTime[0:2] + "50"
    userDiv = "0001"
    reqEmpNo = os.getenv("empNo")

    holidays = get_holiday()


def create_session():
    session = requests.session()
    login_info = {
        "id": os.getenv("id"),
        "pass": os.getenv("pass")
    }
    res = session.post("https://talk.tmaxsoft.com/loginAction.do", data=login_info)

    return session


def get_holiday():
    # 한국천문연구원_특일 정보 - 공휴일 정보 조회
    key = os.getenv("key")
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50" \
          "&solYear=" + str(useStDate)[0:4] + "&solMonth=" + str(useStDate)[4:6] \
          + '&ServiceKey=' + key
    res = requests.get(url)
    json_ob = json.loads(res.text)
    holiday_list = []
    temp = json_ob['response']['body']['items']

    if len(temp) == 0:
        pass
    elif type(temp['item']) == list:
        for holiday in json_ob['response']['body']['items']['item']:
            holiday_list.append(str(holiday['locdate']))
    else:
        holiday_list.append(str(temp['item']['locdate']))

    return holiday_list


async def send_message(useDateStr):
    bot = telegram.Bot(os.getenv("bot_token"))
    await bot.sendMessage(chat_id=os.getenv("chat_id"), text=useDateStr + " 예약 성공")


def book():
    for i in range(30):
        useDate = str(int(useStDate) + i)

        # 지난 날짜 체크
        if int(useDate) < int(datetime.date.today().strftime("%Y%m%d")):
            print(useDate + ' is already past')
            continue

        # 주말 체크
        if datetime.date(int(useDate[0:4]), int(useDate[4:6]), int(useDate[6:8])).weekday() > 4:
            print(useDate + ' is weekend')
            continue

        # 공휴일 체크
        if useDate in holidays:
            print(useDate + ' is holiday')
            continue

        url = "https://talk.tmaxsoft.com/front/health/insertHealth.do?" \
              + "helMngerCd=" + helMngerCd \
              + "&useDate=" + useDate \
              + "&useStTime=" + useStTime \
              + "&useEdTime=" + useEdTime \
              + "&userDiv=" + userDiv \
              + "&reqEmpNo=" + reqEmpNo

        try:
            res = create_session().get(url)
            if res.json()["resultCount"] == '1':
                asyncio.run(send_message(useDate))
                print(useDate + " 예약 성공")
            else:
                print(useDate + " " + str(res.json()['errorMsg']))
        except:
            print(useDate + ' error')


def main():
    init()
    book()


if __name__ == "__main__":
    main()
