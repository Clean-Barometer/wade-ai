FROM python:3.6

ENV FLASK_APP=app
ENV FLASK_DEBUG=1

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-w", "3", "-b", ":5000",\ 
     "-t", "360",\
     "--log-level" ,"DEBUG","--reload", "wsgi:app"]

