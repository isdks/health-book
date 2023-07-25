# health-book
## Getting Started
1. Intall python package
    ```
    pipenv install
    ```
2. Get holiday API key at
[공공데이터포털 - 한국천문연구원_특일 정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012690)
4. Set up ```.env```

## Crontab (Linux)
### Add cron
```bash
crontab -e
```
Add ```0 9 25 * * /{your_directory}/health-book/health.sh 25 >> /{your_directory}/health-book/health.log 2>&1```

## `.env` example
```bash
# 사원 정보
empNo="20230000"
id="gildong_hong"
pass="your password"
# 예약 정보
helMnger="관리사이름"
useMonth=202307
useStDate=1
useStTime=1700
# apis.data.go.kr
key="apis.data.go.kr key"
# telegram
chat_id=7354547234
bot_token="1242345370:AAFaegro-Bg7OUU-jWfZ_jDFV3agea2AvEYY"
# 선호 요일
priority=목월수금
```
