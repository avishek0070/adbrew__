# ======================
# Backend (Django API)
# ======================
FROM python:3.8 AS api

WORKDIR /app

ENV PYTHONPATH=/src
ENV ENV_TYPE=staging
ENV MONGO_HOST=mongo
ENV MONGO_PORT=27017

COPY src/requirements.txt /requirements.txt
RUN pip install --upgrade pip==23.0.1 setuptools==65.5.1 wheel==0.38.4 \
    && pip install -r /requirements.txt




COPY src /src

CMD ["bash", "-c", "cd /src/rest && python manage.py runserver 0.0.0.0:8000"]


# ======================
# Frontend (React)
# ======================
FROM node:14 AS app

WORKDIR /app

COPY src/app ./src/app

CMD ["bash", "-c", "cd src/app && npm install && npm start"]
