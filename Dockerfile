FROM python:3.9

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN apt update
RUN apt install -y libpq-dev build-essential libgl1-mesa-dev
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT []
CMD pipenv run uvicorn main:app --host 0.0.0.0 --reload
