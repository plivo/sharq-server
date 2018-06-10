FROM python:2.7
RUN mkdir -p /opt/sharq-server
WORKDIR /opt/sharq-server
COPY . /opt/sharq-server
RUN apt-get update && apt-get install -y nginx && pip install virtualenv envtpl
RUN virtualenv /opt/sharq-server
RUN . /opt/sharq-server/bin/activate && /opt/sharq-server/bin/pip install --no-cache-dir -r /opt/sharq-server/requirements.txt && /opt/sharq-server/bin/python setup.py install -f && /opt/sharq-server/bin/pip install uwsgi
ADD src/config /etc/sharq-server/config
ADD src/config/nginx.conf /etc/nginx/nginx.conf
ADD src/config/nginx-sharq.conf /etc/nginx/conf.d/sharq.conf
ADD src/config/sharq-server-basicauth /etc/nginx/config.d/sharq-server-basicauth
RUN mkdir /var/run/sharq/
STOPSIGNAL SIGTERM
CMD [ "sh", "-c", "envtpl < /etc/sharq-server/config/sharq.conf.tpl > /etc/sharq-server/config/sharq.conf && cat /etc/sharq-server/config/sharq.conf && /opt/sharq-server/bin/uwsgi --ini /etc/sharq-server/config/sharq.ini && nginx -g 'daemon off;'"]