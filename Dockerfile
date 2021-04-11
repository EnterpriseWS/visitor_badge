# DO NOT run print_badge.service when this container is running
FROM ubuntu:20.04 AS print_badge

RUN apt update -y && \
    apt install -y python3-pip && \
    # *** No need to install fonts if provided in Python code
    # apt install -y ttf-mscorefonts-installer && \
    apt install -y uwsgi && \
    apt install -y uwsgi-plugin-python3

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /
ENV RUNNING_IN_DOCKER=True
EXPOSE 8080
CMD ["uwsgi", "--http-socket", "0.0.0.0:8080", \
              "--plugin", "python3", \
              "--module", "main:app"]
