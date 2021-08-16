FROM python:3.9-buster
#FROM python:3.7.3-alpine22x

#Install curl for healthcheck
RUN apt-get update && apt-get -y install curl

RUN pip3 install --upgrade pip
COPY ./requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY ./app /app
WORKDIR /app

# used to setup testing env
ENV INSIDE_CONTAINER Yes

# healthcheck uri ping - uses curl
HEALTHCHECK CMD curl --fail http://localhost/_health/self || exit 1   

#CMD ["gunicorn"  , "--bind", "0.0.0.0:80", "--access-logfile", "-", "main:app"]
CMD ["gunicorn"  , "--config", "/app/gunicorn.conf.py", "main:app"]
