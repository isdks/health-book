# health-book
## Getting Started
1. Intall python package
    ```
    pipenv install
    ```
2. Set up ```.env```
## To get holiday API key
[공공데이터포털 - 한국천문연구원_특일 정보](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012690)
## Crontab (Linux)
### Add cron
```bash
crontab -e
```
Add ```0 9 25 * * /{your_directory}/health-book/health.sh 25 >> /{your_directory}/health-book/health.log 2>&1```
