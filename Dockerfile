FROM python:3-slim

WORKDIR /bot

COPY ./bot /bot
COPY ./src/config.py /bot

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
