FROM python:3-slim

WORKDIR /bot

COPY ./git-tmp/src/requirements.txt .

RUN pip install -r requirements.txt

COPY ./dumped ./dumped
COPY ./git-tmp/src .
COPY ./src/config.py .

CMD ["python", "main.py"]
