# NYPR Crowdsourcing

## Development

### Prerequisites

You will need the following software properly installed on your computer. Please follow all the directions as written on the websites of these projects and do not neglect to install their dependencies.

* [Git](http://git-scm.com/downloads)
* [Docker](https://docs.docker.com/)

### Getting started

Clone the repo.
```sh
$ git clone git@github.com:nypublicradio/crowdsourcing
$ cd crowdsourcing
```

Create an .env file for environment variables
```sh
$ cp .env.sample .env
```


Build the image.
```sh
$ docker-compose build
```

Run the development server.
```sh
$ docker-compose up
```

Run the migrations.
```sh
$ docker-compose exec django manage.py migrate
```

Create a superuser.
```sh
$ docker-compose exec django manage.py createsuperuser
```

### Running tests

Tests are executed via pytest using NYPR's setuptools extensions.
Use `exec` to run tests on running development containers and `run` to run tests within a new container.
```sh
$ docker-compose exec django python setup.py test
```

For faster testing in development, test dependencies can be permanently
installed.
```sh
$ docker-compose exec django python setup.py test_requirements
```

### Interactive debugging

To enable `ipdb` breakpoints developers need to attach to the Docker container
running the Django development server.

Start the containers and detach from the log output.
```sh
$ docker-compose up -d
```

If using `ipdb` for debugging it will need to be installed in the development container.
```sh
$ docker-compose exec django pip install ipdb
```

Attach to the container. The example below provides the likely name for the Django
container, but if incorrect it can be obtained via `docker-compose ps`.
```sh
$ docker attach crowdsourcing_django_1
```

### Alternate workflow

For developers who prefer to run the Django server directly on their local system
an alternate workflow is available.

Create and activate a virtual environment.
```sh
$ virtualenv ~/.virtualenvs/crowdsourcing
$ . ~/.virtualenvs/crowdsourcing/bin/activate
```

Install the package dependencies and (optionally) the test dependencies.
```sh
$ pip install -e .
$ python setup.py test_requirements
```

Start a Postgres container in the background.
This will expose Postgres on localhost port 5432.
Exclude the `-v ...` argument to avoid persisting data over multiple container runs.
```sh
$ docker run -v /tmp/postgres:/var/lib/postgresql/data -dp 5432:5432 postgres
```

Set environment variables to target postgres container.
The four commands below and any other development config
can be added to the virtual environment's `bin/activate`
script to automate this moving forward.
```sh
$ export DB_HOST=localhost
$ export DB_NAME=postgres
$ export DB_USER=postgres
$ export DB_PASSWORD=
```

Execute the Django initialization commands.
```sh
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver 0.0.0.0:8080
```

## Configuration

Configuration should be set via environment variables.

| **Config Value**          | **Description**                                 |
| ------------------------- | ----------------------------------------------- |
| `AWS_ACCESS_KEY_ID`       | _Set via boto3 config or environment variable._ |
| `AWS_DEFAULT_REGION`      | _Set via boto3 config or environment variable._ |
| `AWS_SECRET_ACCESS_KEY`   | _Set via boto3 config or environment variable._ |
| `AWS_S3_CUSTOM_DOMAIN`    | Cloudfront domain alias for static files.       |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket for Django's storage backend.         |
| `DB_HOST`                 | IP or hostname of the database.                 |
| `DB_NAME`                 | Database name (for app, not tests).             |
| `DB_PASSWORD`             | Database password (for app, not tests).         |
| `DB_USER`                 | Database user (for app, not tests).             |
| `DJANGO_URL_PREFIX`       | URL route to service (/crowdsourcing in prod).  |
| `DJANGO_SECRET_KEY`       | Securely generated key for internal Django use. |
| `SENTRY_DSN`              | URL for reporting uncaught exceptions.          |
