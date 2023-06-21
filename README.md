# health-book
## Crontab (Linux)
### Add cron
```bash
crontab -e
```
Add ```0 9 25 * * /{your_directory}/health-book/health.sh 25```
### Log
```bash
cat /var/log/syslog | grep CRON
