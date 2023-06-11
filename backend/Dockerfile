FROM python:3.11
LABEL authors="chrishultin"

RUN mkdir /app

WORKDIR /app

ADD Pipfile Pipfile.lock ./

RUN pip install pipenv

RUN pipenv install

COPY interactivemaps_api ./interactivemaps_api

ENV PYTHONPATH=$PYTHONPATH:/app

ENTRYPOINT ["pipenv", "run", "uvicorn", "interactivemaps_api.api:app", "--reload", "--host", "0.0.0.0"]