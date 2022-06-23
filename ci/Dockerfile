FROM python:3.7-slim-buster

ENV CONSUL_TEMPLATE_VERSION 0.19.5

# Install Nginx
# Ref: https://github.com/tiangolo/uwsgi-nginx-docker/blob/master/docker-images/install-nginx-debian.sh
COPY scripts/install-nginx-debian.sh /
RUN bash /install-nginx-debian.sh

# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Install depedencies like supervisord, curl, etc.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git supervisor curl python3-dev \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# Install consul-template
RUN curl -L https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.tgz | tar -C /usr/sbin -xzf -

# Install Python requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy configurations to the container
WORKDIR /app
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/nginx-sharq.conf /etc/nginx/conf.d/sharq.conf
COPY config/sharq-server-basicauth /etc/nginx/conf.d/sharq-server-basicauth
COPY config /app/config 

# Copy application code to the container
COPY sharq_server /app/sharq_server

# Start supervisord with Nginx and uvicorn
COPY ci/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
