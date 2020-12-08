FROM python:3.8-buster
COPY app /opt/controller
COPY app/config.ini /etc/autoshut/controller.ini
RUN chmod 777 /etc/autoshut/ \
    && chmod 666 /etc/autoshut/*
CMD ["python", "-u", "/opt/controller/__main__.py"]
