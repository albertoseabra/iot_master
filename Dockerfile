FROM python:3.6-slim-stretch

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

COPY ./app_api /app_api
COPY ./requirements.txt /app_api/requirements.txt

WORKDIR /app_api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1883

CMD ["python", "main.py"]
