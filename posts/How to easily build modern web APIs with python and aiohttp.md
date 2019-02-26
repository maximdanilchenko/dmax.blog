In this post I will show how to build and document REST APIs 
with `aiohttp` and `apispec`. 
With help of some decorators and one middleware you can 
build self-documented (using OpenAPI) API with auto-validation 
support out of the box. No yaml-docstrings, just python code.

First, we need to install `aiohttp-apispec`:
```bash
> pip install aiohttp-apispec
```

Than, as usual, create application fabric for your next 
web app and add some routes to it. 
For simplicity, I will do all things in one python file. 
But in real scalable apps it is bad pattern. 

Lets create some toy database and routes for reading it 
and creating new objects in it.

```python
from aiohttp import web


def create_app():
    app = web.Application()
    setup_routes(app)
    app["users"] = []  # In-memory toy-database
    return app


def setup_routes(app: web.Application):
    app.router.add_get("/users", get_users)
    app.router.add_post("/users", create_user)

### Routes

async def get_users(request: web.Request):
    return web.json_response({"users": request.app["users"]})


async def create_user(request: web.Request):
    new_user = await request.json()
    request.app["users"].append(new_user)
    return web.json_response(new_user)


if __name__ == "__main__":
    web_app = create_app()
    web.run_app(web_app)
```

---
*2019-02-25*
