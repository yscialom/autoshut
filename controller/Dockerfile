FROM python:3.8-buster
COPY app/__main__.py /__main__.py
COPY app/config.ini /etc/autoshut/controller.ini
RUN chmod 777 /etc/autoshut/ \
    && chmod 666 /etc/autoshut/controller.ini
CMD ["python","/__main__.py"]
