FROM python:3.9-alpine
WORKDIR async_download_service
COPY requirements.txt .
RUN apk update && apk add zip && pip install -r requirements.txt
COPY . .