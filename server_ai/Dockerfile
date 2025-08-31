FROM python:3.13.1-slim
WORKDIR /app
COPY main.py /app/
COPY .env /app/
COPY requirements.txt /app/
COPY utils/* /app/utils/
COPY kafka_producer/* /app/kafka_producer/
COPY kafka_consumer/* /app/kafka_consumer/
RUN pip install -r requirements.txt
EXPOSE 8002
CMD ["python", "main.py"]