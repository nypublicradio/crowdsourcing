FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY setup.py ./
RUN python setup.py requirements

COPY . ./
RUN python setup.py develop
CMD run_prod
