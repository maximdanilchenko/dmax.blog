<p class="uk-text-italic">6 Mar 2019</p>

Multi-stage builds are very useful to optimize usage of Dockerfiles
for CI and for development process.
You can make multiple stages using <strong>FROM</strong> statements, 
inherit them by name (given with <strong>as name</strong> statement) or
selectively copy artifacts from one stage to another.

You can see official 
[documentation](https://docs.docker.com/develop/develop-images/multistage-build/#use-multi-stage-builds) 
for example about using multi-stage builds for copying artifacts.

But one of the my favourite use-case is dividing Dockerfile
on stages for different build environments, 
like test, dev, prod and so on, like this:

```docker
FROM python:3.6-alpine3.9 as builder
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

Next we can build image from <strong>test</strong>, <strong>deploy</strong> 
or even <strong>builder</strong> stage:

```bash
> docker build --target test --tag tester
```

---

If you find something wrong in this post fill free to create issues [here](https://github.com/maximdanilchenko/dmax.blog/issues).
