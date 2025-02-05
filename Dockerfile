FROM python:3.12.0-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
COPY requirements.txt /app

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt --no-cache-dir

COPY sokol/ /app
WORKDIR /app

CMD ["python", "manage.py", "runserver", "0:5000"]
