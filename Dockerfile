FROM python:3.9

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN apt update
RUN apt install -y libpq-dev build-essential
RUN pip install pipenv
RUN pipenv install
RUN pipenv install opencv-python

ENTRYPOINT []
CMD pipenv run uvicorn main:app --host 0.0.0.0 --reload
