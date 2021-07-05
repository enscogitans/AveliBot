FROM python:3.8

WORKDIR app
COPY . .

RUN apt-get update && apt-get install -y pipenv && pipenv install --deploy --system

CMD alembic upgrade head && python -m src
