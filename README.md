# Карта ДТП

Проект "Карта ДТП" (https://dtp-stat.ru) 

Обсуждение проекта - https://t.me/crash_map

## Installation

### Requirements

- Python 3.7
- Postgres 11
- docker
- docker-compose
- docker-machine (for win & mac)

### Usage

`docker-compose up -d --build`

### Configure project

Project configured by .dockerenv file in docker folder.
Copy .dockerenv.example and set variables.

[Secret key generator](https://www.lastpass.com/ru/password-generator) recomended length 50 symbols.


First time need create superuser

Run this and follow instructions:

```bash
$ docker-compose exec app ./manage.py createsuperuser --email admin@localhost --username admin
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
