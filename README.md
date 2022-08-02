How to run project:
1. Change environment variables in docker-compose.yml
      POSTGRES_PASSWORD - password that you set in environment of db service
      POSTGRES_HOST - name of db  service
      BOT_TOKEN: your tg bot's token
      ADMINS: ids of users who recieve notifications about outdated delivery time *example: 123456,2345678,14256*
      MAILING_TIME: time of mailing notifications *example '8:00' (must be in '')*
      FROM_TABLE: source google sheet
      TO_TABLE: your google sheet
2. Change TZ in Dockerfile
2. Run __docker-compose up --build__ in terminal.
