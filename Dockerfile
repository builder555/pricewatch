ARG PYTHON_VERSION=3.11.5
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN apt update && apt upgrade -y \
    && apt install cron -y \
    && python -m pip install beautifulsoup4 requests python-telegram-bot

RUN echo "0 */4 * * * cd /app && /usr/local/bin/python main.py >> /tmp/pricelog.txt 2>&1" | crontab -

EXPOSE 8700

ENTRYPOINT ["/app/entrypoint.sh"]
