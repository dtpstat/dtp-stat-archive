# Карта ДТП

Проект "Карта ДТП" (https://dtp-stat.ru) 

Обсуждение проекта - https://t.me/crash_map

## Installation

### Requirements

- Python 3.6.3
- Postgres 10.6

### Quick Install (Linux/macOS)

**Step 1**. Install [pyenv](https://github.com/pyenv/pyenv) 

`pyenv` helps to simple manage Python versions (you can use several 
versions on one machine). Detailed guide about `pyenv` installation 
you can view [here](https://github.com/pyenv/pyenv-installer#prerequisites).

For install `pyenv` just run: 

```bash
$ curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Note: If you do not want to install additional software just install 
`Python 3.6.3` in any way possible. Next steps describe process with 
installed `pyenv`. 

**Step 2**. Install Python with `pyenv`

To install specific version of Python just run:

```bash
$ pyenv install 3.6.3
```

To check that Python successfully installed:

```bash
$ pyenv which python
/Users/some-user/.pyenv/versions/3.6.3/bin/python
```

This operation will not change global version of Python. This must be 
safe.

**Step 3**. Create [virtualenv](https://github.com/pypa/virtualenv)

This step helps to isolate project requirements from global packages.

Install virtualenv:

```bash
$ `pyenv which pip` install virtualenv
```

Create a virtual environment:

```bash
$ `pyenv which virtualenv` --no-site-packages -p `pyenv which python` env
```

**Step 4**. Install project requirements

To install requirements locally you must activate your virtual 
environment:

```bash
$ . env/bin/activate
```

... and then install the requirements:

```bash
$ pip install -r requirements.txt 
```

**Step 5**. Run [PostgreSQL](https://www.postgresql.org)

For quickstart you can use [Docker](https://www.docker.com) image from 
[official Docker Hub repo](https://hub.docker.com/_/postgres/).

To install Docker read [manual](https://docs.docker.com/install/#supported-platforms).

To run PostgreSQL:

```bash
$ docker container run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=MySuperSecretPassword123 \
    -p 127.0.0.1:5432:5432 \
    postgres:10.6
```

Create database for project:

```bash
$ docker container exec -it postgres psql -U postgres -c 'create database "dtp_db"'
```

**Step 6**. Configure project

[Generate](https://www.lastpass.com/ru/password-generator) secret key 
with 50 symbols, copy it, and then:

```bash
$ mkdir -p dtpmap/etc
$ cat <<EOF > dtpmap/etc/secret_key.txt
YOUR-SECRET-KEY
EOF 
```

Create database configuration (hostname port name user password):

```bash
$ echo "localhost 5432 dtp_db postgres MySuperSecretPassword123" > dtpmap/etc/database.txt
```

**Step 7**. Run [Django migrations](https://docs.djangoproject.com/en/2.1/topics/migrations/)

Apply migrations on database:

```bash
$ ./manage.py migrate
```

**Step 8**. Create superuser

Run this and follow instructions:

```bash
$ ./manage.py createsuperuser --email admin@localhost --username admin
```

Create `default_cache` table:

```bash
$ ./manage.py createcachetable
```

To check project backend run:

```bash
$ ./manage.py runserver
```

... and authorize on [this](http://127.0.0.1:8000/admin1/) site 


- NPM зависимости: `npm install`
- `npx` пакет глобально: `npm install -g npx`

### Разработка

В дополнение к запуску сервера Django нужно запустить webpack 
`npm start` для генерации JavaScript кода.

### Запуск парсера данных со stat.gibdd.ru

Загрузить техническую информацию (названия разделов)

```bash
$ ./parser.py tech_data
```

Загрузить регионы и районы

```bash
$ ./parser.py regions
```

Загрузить данные по ДТП. Выгружаются только районы второго уровня (не 
крупные регионы, а по районам), у которых в базе стоит `status = True`. 
Таким образом можно выгружать только то, что вам нужно. По дефолту 
`status = True` у всех районов. 

```bash
$ ./parser.py data
```

### Развертывание

Запустите эту команду перед развертыванием для генерации JavaScript 
кода:

```bash
$ npm run build-production
```
