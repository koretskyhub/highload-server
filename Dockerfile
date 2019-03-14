FROM python:3.6

RUN apt-get update
RUN pip install uvloop

RUN  mkdir -p /bin/highload-server
COPY source /bin/highload-server
 
WORKDIR /bin/highload-server

EXPOSE 80

CMD python3 main.py --config-file /etc/httpd.conf
