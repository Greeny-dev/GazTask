FROM python:3.12-slim

USER root

WORKDIR /app

COPY ./requirements.txt .

RUN python3.12 -m pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python3.12", "-u", "src/start.py"]