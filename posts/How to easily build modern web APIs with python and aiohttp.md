*26 Feb 2019*

Thanks to python 3.5+ asyncio we can write concurrent 
code using the async/await syntax. 
It is perfect for IO-bound tasks. 
Since web is mostly IO-bound with asyncio we can build
high performance web apps. There are already several web
frameworks built for it. 
My favourite one is `aiohttp`. It is stable, fast, 
has built-in http client, a lot of third-party tools 
and good maintainers and community.

In this post I will show how to build and document
REST APIs with `aiohttp` and `apispec`. 
With help of two decorators and one middleware 
you can build self-documented API 
with auto-validation support out of the box. 
No yaml-docstrings, just python code.

### 1. Preparation

First, we need to install `aiohttp-apispec`.

```bash
> pip install aiohttp-apispec
```

Than, as usual, create application fabric for your next 
web app. Also lets create some simple toy database, 
so we can add some close-to-reality features.

```python
# app.py
from aiohttp import web

from routes import setup_routes


def create_app():
    app = web.Application()
    setup_routes(app)
    # In-memory toy-database:
    app["users"] = []
    return app


if __name__ == "__main__":
    web_app = create_app()
    web.run_app(web_app)
```

Add some views.

```python
# views.py
from aiohttp import web


async def get_users(request: web.Request):
    return web.json_response(
        {"users": request.app["users"]}
    )


async def create_user(request: web.Request):
    new_user = await request.json()
    request.app["users"].append(new_user)
    return web.json_response(
        {"message": f"Hello user!"}
    )
```

And add it to router.

```python
# routes.py
from aiohttp import web

from views import get_users, create_user


def setup_routes(app: web.Application):
    app.router.add_get("/users", get_users)
    app.router.add_post("/users", create_user)
```

Finally we can run our first version:
```bash
> python main.py
```

### 2. Adding validation
We already can use our API, but it has no validation
of client request content. To add it we need its schema description.
One of the best instruments for it is 
powerful and feature-reach `marshmallow` library. 

We can use it like so:

```python
# schemas.py
from marshmallow import Schema, fields, validate


class User(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    gender = fields.String(
        validate=validate.OneOf(["f", "m"])
    )
```

Next, magic begins. To make our app
validate request to specific view 
with this schema all we need is to add
`@request_schema` decorator to this view.
After that we can find deserialized and 
validated object in `request["data"]`
and use it in our view as we want.

```python
# views.py
from aiohttp import web
from aiohttp_apispec import request_schema

from schemas import User


async def get_users(request: web.Request):
    return web.json_response(
        {"users": request.app["users"]}
    )


@request_schema(User)
async def create_user(request: web.Request):
    new_user = request["data"]
    request.app["users"].append(new_user)
    return web.json_response(
        {"message": f"Hello {new_user['name']}!"}
    )
```

Also we need to initialize `aiohttp-apispec` 
with `setup_aiohttp_apispec` function
and add validation middleware to our app. 
Here you can see optional `swagger_path` argument.
It is path to our documentation page.
 
```python
# app.py
from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec, 
    validation_middleware,
)

from routes import setup_routes


def create_app():
    app = web.Application()
    setup_routes(app)
    # In-memory toy-database:
    app["users"] = []
    
    setup_aiohttp_apispec(app, swagger_path="/docs")
    app.middlewares.append(validation_middleware)
    
    return app


if __name__ == "__main__":
    web_app = create_app()
    web.run_app(web_app)
```

Now restart the app and go to http://localhost:8080/docs.
You can see nice SWAGGER page with all your methods. 
Try to use one. If you will send wrong data, our 
app will answer with 422 code in this case. 
So our validation works. Cool!

Next we need to make out documentation page more informative.

### 3. Customizing documentation
First lets add some schemas needed 
for responses information.

```python
# schemas.py
from marshmallow import Schema, fields, validate


class User(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    gender = fields.String(
        validate=validate.OneOf(["f", "m"])
    )


class Message(Schema):
    message = fields.String()


class UsersList(Schema):
    users = fields.Nested(User(many=True))
```

Use `@docs` decorator to add 
tags, summary, description or responses 
list to our views.

```python
# views.py
from aiohttp import web
from aiohttp_apispec import (
    request_schema, docs
)
from schemas import User, Message, UsersList


@docs(
    tags=["users"],
    summary="Get users list",
    description="Get list of all users from our toy database",
    responses={
        200: {"description": "Ok. Users list", "schema": UsersList},
        404: {"description": "Not Found"},
        500: {"description": "Server error"},
    }
)
async def get_users(request: web.Request):
    return web.json_response(
        {"users": request.app["users"]}
    )


@docs(
    tags=["users"],
    summary="Create new user",
    description="Add new user to our toy database",
    responses={
        200: {"description": "Ok. User created", "schema": Message},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
        500: {"description": "Server error"},
    }
)
@request_schema(User)
async def create_user(request: web.Request):
    new_user = request["data"]
    request.app["users"].append(new_user)
    return web.json_response(
        {"message": f"Hello {new_user['name']}!"}
    )
```

Now restart your app, go to SWAGGER console 
page and use your awesome interactive documentation!

You can find sources [here](https://github.com/maximdanilchenko/dmax.blog/tree/master/sources/01).

---

If you find something wrong in this post fill free to create issues [here](https://github.com/maximdanilchenko/dmax.blog/issues).
