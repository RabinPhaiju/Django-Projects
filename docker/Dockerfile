FROM python:3.11.4-slim-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME
RUN groupadd -g 1000 rbnph \
      && useradd -m -u 1000 -g 1000 -s /bin/bash -d $APP_HOME  rbnph

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y netcat \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY docker/entrypoint.sh /home/entrypoint.sh
RUN sed -i 's/\r$//g' /home/entrypoint.sh
RUN chmod +x /home/entrypoint.sh

RUN chown -R rbnph:rbnph $APP_HOME
USER rbnph

COPY . $APP_HOME
EXPOSE 8000

ENTRYPOINT [ "/home/entrypoint.sh" ]

