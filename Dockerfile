FROM python:3-slim

WORKDIR /bot

COPY ./src/requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .
COPY ./src/config.py .

CMD ["python", "main.py"]
