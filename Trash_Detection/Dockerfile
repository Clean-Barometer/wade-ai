FROM python:3.6

ENV FLASK_APP=app
ENV FLASK_DEBUG=1

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn","wsgi:app"]

