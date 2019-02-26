
Multi-stage Dockerfile:

```docker
FROM python:3.6-alpine3.9 as builder
RUN apk add --no-cache \
git \
make \
gcc \
linux-headers \
libc-dev \
openssl-dev \
libffi-dev \
postgresql-dev \
build-base \
libxslt-dev \
libxml2-dev \
zlib-dev \
jpeg-dev \
bash
ADD requirements.txt /app/
WORKDIR /app
RUN pip3 install --upgrade -r requirements.txt

FROM builder as test
ADD dev-requirements.txt /app/
RUN pip3 install --upgrade -r dev-requirements.txt
EXPOSE 8020
CMD [ "python", "./main.py" ]

FROM builder as deploy
ADD . /app
CMD [ "python", "./main.py" ]
```

Building `test` stage:
```bash
> docker build --target test --tag tester
```
