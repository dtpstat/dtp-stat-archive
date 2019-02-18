[![Build Status](https://travis-ci.com/tadata-ru/dtp-stat.svg?branch=master)](https://travis-ci.com/tadata-ru/dtp-stat)

# Карта ДТП

Проект **"Карта ДТП"** (https://dtp-stat.ru) 

Обсуждение проекта - https://t.me/crash_map

---

## Developer Environment (local)
### Installation
#### Requirements
- Python >=3.6
- Postgresql >=10.6
- Nodejs (npm)

#### Install dependencies

1. Install node packages
```bash
$ npm install -g npx
$ npm install
```
2. Install python dependencies
```bash
pip install -r requirements.txt
```

#### Prepare and Configure Project
1. Start postgresql server.
2. Create appropriate database and role:
```bash
$ psql -c "CREATE DATABASE django;" -U postgres
$ psql -c "CREATE ROLE django WITH LOGIN PASSWORD 'django';" -U postgres
$ psql -c "ALTER ROLE django CREATEDB;" -U postgres
$ psql -c "GRANT ALL PRIVILEGES ON DATABASE django TO django;" -U postgres
```
3. Export `DATABASE_URL`  (used by app for database connection) and `DEBUG` environment variable with database info according to previous steps:
```bash
$ export DATABASE_URL="postgres://django:django@localhost:5432/django"
$ export DEBUG=true
```
4. Perform migrations:
```bash
$ ./manage.py makemigrations --noinput
$ ./manage.py migrate --noinput
```
5. Create `default_cache` cache table:
```bash
$ ./manage.py createcachetable
```
6. It\`s time to start app:
```bash
$ ./manage.py runserver localhost:8000
```
Authorize on http://127.0.0.1:8000/admin1.

7. You need to run `npm start` together with app to generate JavaScript-code:
```bash
npm start
```

## Developer Environment (docker)
### Installation
#### Requirements
- docker
- docker-compose
- docker-machine (for win & mac)

#### Prepare and Configure Project

Project configured by `.dockerenv` file in docker folder.

Rename `docker/.dockerenv.example` to `docker/.dockerenv` and set variables:

* `SECRET_KEY`, - secret key, you can generate it with:
    * [Secret key generator](https://www.lastpass.com/ru/password-generator) (recomended length: 50 symbols)
    * oneliner: 

```bash
    python3 -c "import random, string; print('SECRET_KEY=\"%s\"'%''.join([random.SystemRandom().choice(\"{}{}{}\".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(63)]))"
```

* `DEBUG`, - set it to `true`

#### Start project
1. Build and up containers: `docker-compose up -d --build`
2. First time need create superuser

Run this and follow instructions:

```bash
$ docker-compose exec app ./manage.py createsuperuser --email admin@localhost --username admin
```

3. Authorize on http://127.0.0.1:8000/admin1.

## Запуск парсера данных со stat.gibdd.ru

Загрузить в базу техническую информацию (названия разделов)

```bash
$ ./parser.py tech_data
```

Загрузить в базу регионы и районы

```bash
$ ./parser.py get_regions
```

Загрузить в базу все ДТП. Для этого нужно предварительно скачать дамп всех ДТП и положить в папку data - https://drive.google.com/file/d/1aUTPLqUX5xZhmtcFODyVb7GpBj3_SHui/view?usp=sharing 

```bash
$ ./parser.py get_dtp
```

Чтобы включить отображение региона нужно в базе данных поставить ему status = True.

## Развертывание

Запустите эту команду перед развертыванием для генерации JavaScript 
кода:

```bash
$ npm run build-production
```


### Старт без Docker и изменения переменных окружения

Если не хочется выкачивать все данные - вот бекап базы https://drive.google.com/open?id=1SPHyY-802U-USRQh3j4JfzhIO86eAaUp
###Backend:
    
- Скопировать `dtpmap/.env.tmpl -> dtpmap/.env`
- Отредактировать `dtpmap/.env`

###Frontend:

(самый простой способ)
- Ставите Node.js https://nodejs.org/en/
- Ставите yarn https://yarnpkg.com/en/docs/install
- В корне проекта выполняете `yarn` и затем `yarn start`

Выполнить `manage.py runserver 8000`
