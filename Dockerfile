FROM python:3-slim

ADD . /bot

WORKDIR /bot
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
CMD ["/bin/bash"]
