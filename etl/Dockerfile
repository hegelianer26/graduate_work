FROM python:3.7-slim

RUN mkdir /etl

COPY requirements.txt /etl/

RUN pip3 install -r etl/requirements.txt --no-cache-dir

COPY . /etl

WORKDIR /etl

CMD ["python3", "main.py"]

# docker-compose в папке infra, exampleenv в django_api