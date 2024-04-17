FROM python:3.10-slim

WORKDIR /assistant

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gunicorn

RUN pip install --upgrade pip --no-cache-dir && pip install -r requirements.txt --no-cache-dir

RUN python3 -m spacy download ru_core_news_sm

COPY . .

CMD ["python", "-m", "gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8090"]
