FROM python:3.10-alpine3.17
LABEL org.opencontainers.image.source="https://github.com/CptKirk/upgrade-pg-extensions"
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt \
    && apk add --no-cache postgresql14-client
ADD upgrade.py upgrade.py