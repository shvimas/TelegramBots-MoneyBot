FROM python:3-slim

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .
COPY config.py .

CMD ["python", "main.py"]