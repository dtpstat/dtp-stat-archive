
# Карта ДТП

Проект "Карта ДТП" (https://dtp-stat.ru) 

Обсуждение проекта - https://t.me/crash_map

## Developer Environment (Docker)
### Installation
#### Requirements
- Python >=3.6
- Postgresql >=10.6
- docker
- docker-compose
- docker-machine (for win & mac)

#### Prepare and Configure Project

Project configured by .dockerenv file in docker folder.

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


### Старт без Docker
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
