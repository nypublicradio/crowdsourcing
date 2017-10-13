# crowdsourcing microservice

## development

### build the image
`$ docker-compose build`

_Use this to rebuild the image if requirements or the Dockerfile change_

### run the migrations
`$ docker-compose run django manage.py migrate`

### make yourself a superuser
`$ docker-compose run django manage.py createsuperuser`

### run
`$ docker-compose up`

### debug
Use the `--service-ports` argument to enable breakpoints

```python3
# some code
import ipdb; ipdb.set_trace()
```

`$ docker-compose run --service-ports --rm django`

### test
`$ docker-compose run --rm django manage.py test`

## production

### settings to expose via environment variables

#### aws keys
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION
```

#### aws s3 bucket and cloudfront domain (without path) for static files
```
AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN
```

#### postgres connection information
```
DB_HOST
DB_NAME
DB_PASSWORD
DB_USER
```

#### url route to microservice (ie. /crowdsourcing)
```
DJANGO_URL_PREFIX
```

#### securely generated secret key
```
DJANGO_SECRET_KEY
```

#### sentry project
```
SENTRY_DSN
```
