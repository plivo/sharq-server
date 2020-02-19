FROM python:2.7

ENV CONSUL_TEMPLATE_VERSION 0.19.5
RUN mkdir -p /opt/sharq-server
WORKDIR /opt/sharq-server
COPY . /opt/sharq-server
RUN mkdir /etc/supervisord && mkdir /etc/supervisord/conf.d && mkdir /var/log/supervisord && pip install supervisor
RUN apt-get update && apt-get install -y nginx && pip install virtualenv envtpl

RUN curl -L https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.tgz | tar -C /usr/sbin -xzf -
RUN virtualenv /opt/sharq-server
RUN . /opt/sharq-server/bin/activate && /opt/sharq-server/bin/pip install --no-cache-dir -r /opt/sharq-server/requirements.txt && /opt/sharq-server/bin/python setup.py install -f && /opt/sharq-server/bin/pip install uwsgi

ADD src/config /etc/sharq-server/config
ADD src/config/nginx.conf /etc/nginx/nginx.conf
ADD src/config/nginx-sharq.conf /etc/nginx/conf.d/sharq.conf
ADD src/config/sharq-server-basicauth /etc/nginx/conf.d/sharq-server-basicauth

COPY src/config/sharq.conf.ctmpl /etc/sharq-server/config/sharq.conf.ctmpl
COPY src/config/sharq.ini.ctmpl /etc/sharq-server/config/sharq.ini.ctmpl
COPY src/config/sharq.ini.ctmpl /etc/sharq-server/config/sharq.ini
COPY src/config/supervisord.conf /etc/supervisord.conf
RUN mkdir /var/run/sharq/

COPY ci/entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh && \
	chown root:root /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
