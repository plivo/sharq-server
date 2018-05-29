FROM python:2.7.15-alpine
RUN mkdir -p /opt/sharqserver
WORKDIR /opt/sharqserver
COPY . /opt/sharqserver
RUN pip install virtualenv && apk add --no-cache uwsgi-python
RUN virtualenv /env 
RUN . /env/bin/activate && /env/bin/pip install --no-cache-dir -r /opt/sharqserver/requirements.txt
EXPOSE 8000
ADD src/config /etc/sharq/config
RUN sed -i "s/${SHARQ_REDIS}/$$redishost$$/g" /etc/sharq/config/sharq.conf
ENTRYPOINT [ "/opt/sharqserver/bin/uwsgi", "--ini", "/etc/sharq/config/sharq.ini" ]