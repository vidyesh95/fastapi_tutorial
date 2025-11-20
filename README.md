### Run commands:
```shell

uv init
uv add fastapi --extra standard
uv add pwdlib --extra argon2
uv add pyjwt --extra crypto
uv add python-dotenv
uv add sqlmodel
uv add imagekitio
uv remove
uv lock
uv sync
uv run fastapi dev
uv build
uv lock --upgrade
uv sync
```

### Run with
```shell

uv run fastapi dev app/app.py 
```

or
```shell

uv run main.py 
```
