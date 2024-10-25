FROM python:3.13-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

RUN groupadd -g 1000 systemadmin \
    && useradd -m -u 1000 -g 1000 -s /bin/bash -d $APP_HOME systemadmin

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get install -y netcat \
    && apt-get install -y wget gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Add the PostgreSQL 16 APT repository for(backup)
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv 
COPY Pipfile* .

# Install dependencies
RUN pipenv install --system --deploy

COPY docker/entrypoint.sh /home/entrypoint.sh
RUN sed -i 's/\r$//g' /home/entrypoint.sh
RUN chmod +x /home/entrypoint.sh

RUN chown -R systemadmin:systemadmin $APP_HOME
USER systemadmin

# Copy application code
COPY . $APP_HOME

# Expose port
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["/home/entrypoint.sh"]