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

    with open('helMngerInfo.json', 'r') as file:
        helMngerCdMap = json.load(file)

    helMnger = os.getenv("helMnger")
    helMngerCd = helMngerCdMap[helMnger]
    useMonth = os.getenv("useMonth")
    useStDate = os.getenv("useStDate")
    useEdDate = calendar.monthrange(int(useMonth[0:4]), int(useMonth[4:6]))[1]
    useStTime = os.getenv("useStTime")
    useEdTime = useStTime[0:2] + "50"
    userDiv = "0001"
    reqEmpNo = os.getenv("empNo")

    if len(sys.argv) == 1:
        holidays = get_holiday(useMonth)
    elif sys.argv[1] == '25':
        next_month = (datetime.date.today() + relativedelta(months=1)).strftime('%Y%m')
        holidays = get_holiday(next_month)

    session = create_session()


def create_session():
    rs = requests.session()
    login_info = {
        "id": os.getenv("id"),
        "pass": os.getenv("pass")
    }
    res = rs.post("https://talk.tmaxsoft.com/loginAction.do", data=login_info)

    return rs


def get_holiday(date):
    # 한국천문연구원_특일 정보 - 공휴일 정보 조회
    key = os.getenv("key")
    apis_url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json&numOfRows=50" \
               "&solYear=" + date[0:4] + "&solMonth=" + date[4:6] \
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


async def send_message(message):
    bot = telegram.Bot(os.getenv("bot_token"))
    await bot.sendMessage(chat_id=os.getenv("chat_id"), text=message)


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


class Result(object):
    def __init__(self, is_sucess=False, data=""):
        self.is_sucess = is_sucess
        self.data = data


def request_book(useDate):
    if not is_valid_date(useDate):
        return Result()

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
            msg = useDate + " 예약 성공"
            print(msg)
            return Result(True, msg)
        else:
            msg = useDate + " " + str(res.json()['errorMsg'])
            print(msg)
            return Result(False, msg)
    except:
        print(useDate + ' error')


def book0():
    res = []
    for i in range(int(useStDate), int(useEdDate) + 1):
        use_date = str(int(useMonth) * 100 + i)
        if request_book(use_date).is_sucess:
            res.append(use_date + " 예약 성공")
    return res


def book25():
    # 25일에 사용
    next_month = (datetime.date.today() + relativedelta(months=1)).strftime('%Y%m')
    useEdDate = calendar.monthrange(int(next_month[0:4]), int(next_month[4:6]))[1]
    dow_dict = {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4, '토': 5}

    priority = os.getenv('priority')
    if not priority:
        print("priority is null")
        return

    dates = []
    for dow in priority:
        wd = dow_dict[dow]
        for i in range(1, int(useEdDate) + 1):
            use_date = int(next_month) * 100 + i
            if datetime.date(use_date // 10000, use_date % 10000 // 100, use_date % 100).weekday() == wd:
                dates.append(str(use_date))

    res = []
    for date in dates:
        res.append(request_book(date).data)
    return res


def main():
    init()
    res = []
    if len(sys.argv) == 1:
        res = book0()
    elif sys.argv[1] == '25':
        res = book25()

    if res:
        asyncio.run(send_message('\n'.join(res)))


if __name__ == "__main__":
    main()
