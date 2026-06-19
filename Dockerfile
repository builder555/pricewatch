FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN apk update \
    && apk add --no-cache cronie firefox-esr \
    && uv export --frozen --no-dev --no-emit-project -o requirements.txt \
    && uv pip install --system --no-cache -r requirements.txt

COPY . .

RUN mkdir -p /app/app/db/data

RUN echo "0 */4 * * * . /etc/environment; cd /app && /usr/local/bin/python main.py >> /tmp/pricelog.txt 2>&1" | crontab -

EXPOSE 8700

ENTRYPOINT ["/app/entrypoint.sh"]
