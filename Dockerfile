FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apk update \
    && apk add --no-cache cronie \
    && python -m pip install beautifulsoup4 requests python-telegram-bot \
    && mkdir -p /app/app/db/data

RUN echo "0 */4 * * * . /etc/environment; cd /app && /usr/local/bin/python main.py >> /tmp/pricelog.txt 2>&1" | crontab -

EXPOSE 8700

ENTRYPOINT ["/app/entrypoint.sh"]
