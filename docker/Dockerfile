FROM python:3.6-slim-buster

RUN mkdir -p /opt/sharq-server
WORKDIR /opt/sharq-server
COPY . /opt/sharq-server
RUN mkdir /etc/supervisord && mkdir /etc/supervisord/conf.d && mkdir /var/log/supervisord && pip install supervisor
RUN apt-get update && apt-get install -y make nginx g++ git && pip install virtualenv envtpl

RUN virtualenv /opt/sharq-server
RUN . /opt/sharq-server/bin/activate && /opt/sharq-server/bin/pip install --no-cache-dir -r /opt/sharq-server/requirements.txt && /opt/sharq-server/bin/python setup.py install -f

ADD docker/config /etc/sharq-server/config
ADD docker/config/nginx.conf /etc/nginx/nginx.conf
ADD docker/config/nginx-sharq.conf /etc/nginx/conf.d/sharq.conf
ADD docker/config/sharq-server-basicauth /etc/nginx/conf.d/sharq-server-basicauth

COPY docker/config/sharq.conf /etc/sharq-server/config/sharq.conf
COPY docker/config/sharq.ini /etc/sharq-server/config/sharq.ini
COPY docker/config/supervisord.conf /etc/supervisord.conf
RUN mkdir /var/run/sharq/

ENTRYPOINT [ "supervisord", "-c", "/etc/supervisord.conf" ]
