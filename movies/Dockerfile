FROM python:3.8-slim

WORKDIR /fastapi

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gunicorn

RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir

COPY ./src .

CMD ["python", "-m", "gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]