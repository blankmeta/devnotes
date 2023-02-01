FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install --reinstall libpq-dev python3-dev -y

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "devnotes.wsgi:application", "--bind", "0:8000" ]

LABEL author="blankmeta"