FROM python:3.9.7-slim-buster

WORKDIR /usr/src/app
ENV FLASK_APP=app

COPY /app ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["flask","run","--host=0.0.0.0"]
