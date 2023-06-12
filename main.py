import os
import sys
import requests
import asyncio
import telegram
import json
import datetime
from dotenv import load_dotenv
import calendar
from dateutil.relativedelta import relativedelta


def init():
    load_dotenv()

    global useMonth
    global useStDate
    global useEdDate
    global helMngerCd
    global useStTime
    global useEdTime
    global userDiv
    global reqEmpNo
    global holidays
    global session

    helMngerCdMap = {
        "손애화": "HEL20220609001",
        "이승우": "HEL20140101130",
        "정영민": "HEL20210330001",
        "남경인": "HEL20230125001",
    }

    helMnger = os.getenv("helMnger")
    helMngerCd = helMngerCdMap[helMnger]
    useMonth = os.getenv("useMonth")
    useStDate = os.getenv("useStDate")
    useEdDate = calendar.monthrange(int(useMonth[0:4]), int(useMonth[4:6]))[1]
    useStTime = os.getenv("useStTime")
    useEdTime = useStTime[0:2] + "50"
    userDiv = "0001"
    reqEmpNo = os.getenv("empNo")

    holidays = get_holiday()

    session = create_session()


def create_session():
    rs = requests.session()
    login_info = {
        "id": os.getenv("id"),
        "pass": os.getenv("pass")
    }
    res = rs.post("https://talk.tmaxsoft.com/loginAction.do", data=login_info)

    return rs


def get_holiday():
    # 한국천문연구원_특일 정보 - 공휴일 정보 조회
    key = os.getenv("key")
    apis_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50" \
               "&solYear=" + str(useStDate)[0:4] + "&solMonth=" + str(useStDate)[4:6] \
               + '&ServiceKey=' + key
    res = requests.get(apis_url)
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


def is_valid_date(date):
    # 지난 날짜 체크
    if int(date) < int(datetime.date.today().strftime("%Y%m%d")):
        print(date + ' is already past')
        return False

    # 주말 체크
    if datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])).weekday() > 4:
        print(date + ' is weekend')
        return False

    # 공휴일 체크
    if date in holidays:
        print(date + ' is holiday')
        return False

    return True


def request_book(useDate):
    if not is_valid_date(useDate):
        return

    url = "https://talk.tmaxsoft.com/front/health/insertHealth.do?" \
          + "helMngerCd=" + helMngerCd \
          + "&useDate=" + useDate \
          + "&useStTime=" + useStTime \
          + "&useEdTime=" + useEdTime \
          + "&userDiv=" + userDiv \
          + "&reqEmpNo=" + reqEmpNo

    try:
        res = session.get(url)
        if res.json()["resultCount"] == '1':
            asyncio.run(send_message(useDate))
            print(useDate + " 예약 성공")
        else:
            print(useDate + " " + str(res.json()['errorMsg']))
    except:
        print(useDate + ' error')


def book0():
    for i in range(int(useStDate), int(useEdDate) + 1):
        use_date = str(int(useMonth) * 100 + i)
        request_book(use_date)


def book25():
    # 25일에 사용
    week_day = os.getenv('week_day_bit')
    next_month = (datetime.date.today() + relativedelta(months=1)).strftime('%Y%m')
    if not week_day:
        print("week_day_bit is null")
        return

    dates = []
    for i in range(int(useStDate), int(useEdDate) + 1):
        use_date = str(int(next_month) * 100 + i)
        if int(week_day[datetime.date(int(use_date[0:4]), int(use_date[4:6]), int(use_date[6:8])).weekday()]):
            dates.append(use_date)

    for date in dates:
        request_book(date)


def main():
    init()
    if len(sys.argv) == 1:
        book0()
    elif sys.argv[1] == '25':
        book25()


if __name__ == "__main__":
    main()
