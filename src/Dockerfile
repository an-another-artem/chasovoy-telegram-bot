FROM python:3.10.17-alpine3.21
COPY ../src /tg-bot/
RUN pip install -r /tg-bot/requirements.txt
CMD [ "python3 /tg-bot/main.py" ]