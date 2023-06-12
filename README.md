# Algs1

## Local dev environment

Actiavte your python virtual environment to avaoid clashing with other installed packages. If you haven't tried before, try the command below (for windows users).

```sh
> python3 -m venv <path to .virtualenvs>\Algs1

> <path to .virtualenvs>\Algs1\Scripts\activate.ps1 
```

For more information on venv, see: https://docs.python.org/3/library/venv.html#module-venv

Once venv is created on Algs1 directory, we can go ahead to install the required packages.

```sh
> python3 -m pip install -r requirements.txt

# to run
> python3 manage.py runserver
```

To run test suite, change directory to src folder and execute command 'pytest'

```
> pytest
```

# Docker compose
to run container

```sh
> docker compose up
```