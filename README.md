# crowdsourcing microservice

## development

### build the image
`$ docker build -t nypr-crowdsourcing .`

_Use this to rebuild the image if requirements or the Dockerfile change_

### run the migrations
`$ docker-compose run django ./manage.py migrate`

### run
`$ docker-compose up`

### debug
Use the `--service-ports` argument to enable breakpoints

```python3
# some code
import ipdb; ipdb.set_trace()
```

`$ docker-compose up --service-ports`
