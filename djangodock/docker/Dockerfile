FROM python:3.13-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV APP_HOME /home/app/web
WORKDIR $APP_HOME

RUN groupadd -g 1000 djangodock \
    && useradd -m -u 1000 -g 1000 -s /bin/bash -d $APP_HOME djangodock

RUN pip install pipenv 

# Copy Pipfile
COPY Pipfile* .

# Install dependencies
RUN pipenv install --system --deploy

COPY docker/entrypoint.sh /home/entrypoint.sh
RUN sed -i 's/\r$//g' /home/entrypoint.sh
RUN chmod +x /home/entrypoint.sh

RUN chown -R djangodock:djangodock $APP_HOME
USER djangodock

# Copy application code
COPY . $APP_HOME

# Expose port
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["/home/entrypoint.sh"]