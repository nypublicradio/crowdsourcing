FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . ./
RUN pip install -e .

CMD run_prod
