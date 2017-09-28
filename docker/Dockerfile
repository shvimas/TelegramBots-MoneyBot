FROM python:3-slim

WORKDIR /bot/src

COPY ../bot /bot
COPY ../src/config.py /bot/src

RUN pip install -r requirements.txt

CMD ["/bin/bash"]
