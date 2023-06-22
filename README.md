# health-book
## Getting Started
1. Intall python package
    ```
    pipenv install
    ```
2. Set up ```.env```
## Crontab (Linux)
### Add cron
```bash
crontab -e
```
Add ```0 9 25 * * /{your_directory}/health-book/health.sh 25 >> /{your_directory}/health-book/health.log 2>&1```
