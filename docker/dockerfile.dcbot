FROM python:3.13-alpine

WORKDIR /discord-bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache ffmpeg

COPY . .

CMD ["python", "bot.py"]