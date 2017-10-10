FROM python:2.7

WORKDIR /pythonapp

ADD clairvoyance.py /
ADD . .

RUN pip install pyKML

VOLUME /pythonapp

EXPOSE 1337

CMD ["python", "./clairvoyance.py"]