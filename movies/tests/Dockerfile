FROM python:3.8-slim

WORKDIR /tests

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gunicorn

RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir

COPY ./functional .

ENTRYPOINT ["sh", "-c", "python utils/wait_for_es.py && python utils/wait_for_redis.py && pytest src"]
