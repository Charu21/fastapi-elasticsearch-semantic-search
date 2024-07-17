FROM python:3.8-slim

RUN apt-get update && apt-get install -y netcat

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["./wait-for-it.sh", "elasticsearch:9200", "-t", "30", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
