# eeki-django

django backend for eeki project

## project setup

- clone the repo

  ```bash
  git clone git@bitbucket.org:wireonelabs/eeki-django.git
  ```

- go into the directory

  ```bash
  cd eeki-django
  ```

- create a virtual environment

  ```bash
  python3 -m venv .venv
  ```

- activate virtual environment

  ```bash
  . .venv/bin/activate
  ```

- install requirements

  ```bash
  # for dev environment setup
  pip install -r requirements/dev-requirements.txt

  # for prod environment setup
  pip install -r requirements/dev-requirements.txt
  ```

- go inside `main/` directory

  ```bash
  cd main/
  ```

- create `settings.ini` from `settings.ini.sample`

  ```bash
  cp settings.ini.sample settings.ini
  ```

- inside `settings.ini` change `DEPLOYMENT` to:

  - `test`, for development or testing.

    Under `test` deployment, these fields are ignored:

    - `DATABASE_NAME`
    - `DATABASE_HOST`
    - `DATABASE_PORT`
    - `DATABASE_USER`
    - `DATABASE_PASSWORD`

  - `prod`, for production environments.

    For production enviroments, the above values can be obtained below

## deployment setup

### setup postgres

- install and start postgresql

  ```bash
  sudo apt install postgresql
  sudo systemctl enable --now postgresql.service
  ```

- create db, user and password in postgresql

  ```bash
  sudo su postgres

  psql

  CREATE DATABASE projectName;
  CREATE USER projectUser WITH PASSWORD 'password';
  ALTER ROLE projectUser SET client_encoding TO 'utf8';
  ALTER ROLE projectUser SET default_transaction_isolation TO 'read committed';
  GRANT ALL PRIVILEGES ON DATABASE projectName TO projectUser;
  ```

  Replace projectName and projectUser above with appropriate names.

### setup supervisor

- install and enable supervisor

  ```
  sudo apt install supervisor
  sudo systemctl enable --now supervisor
  ```

- create config file for the project in `/etc/supervisor/conf.d/`:

  ```
  [program:project]
  command=/path/to/project/.venv/bin/gunicorn --bind 127.0.0.1:8000 main.wsgi
  directory=/path/to/project/main
  autostart=true
  autorestart=true
  stderr_logfile=/var/log/myproject.err.log
  stdout_logfile=/var/log/myproject.out.log
  ```

- start the project

  ```bash
  sudo supervisorctl start project
  ```

### setup nginx

- install and enable nginx

  ```bash
  sudo apt install nginx
  sudo systemctl enable --now nginx
  ```

- create an entry point in `/etc/nginx/sites-available/` for our project.(e.g. project).
  complete path would be `/etc/nginx/sites-available/project`

  ```nginx
  server {
      listen 80;

      location /static/ {
                  alias /path/to/project/main/static/;
      }

      location / {
          proxy_pass 127.0.0.1:8000;
      }
  }
  ```

- remove other sites and enable our site

  ```bash
  sudo rm -rf /etc/sites-enabled/*
  sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled/project
  ```

- restart nginx

  ```bash
  sudo systemctl restart nginx
  ```
