FROM python:3-alpine

ENV DISCORD_TOKEN=""
ENV INFURA_PROJECT_ID=""

RUN apk update && \
    apk --no-cache add gcc python3-dev libffi-dev musl-dev

ADD requirements.txt bot.py seeder.json ./

RUN pip install -r requirements.txt

CMD [ "python", "bot.py" ]
