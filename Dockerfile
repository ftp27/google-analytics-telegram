FROM python:3.9-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY *.py .
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/data/credentials.json"

EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
    