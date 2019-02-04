# Карта ДТП
Проект "Карта ДТП" (https://dtp-stat.ru) 

Обсуждение проекта - https://t.me/crash_map

### Установка
- Python 3.6
- Postgres 10  `brew install postgres`
- Зависимости `pip3 install -r requirements.txt`
- Создайте базу данных: 

```
createdb *database_name*
psql *database_name*
CREATE ROLE *role_name* WITH LOGIN PASSWORD *password*;
GRANT ALL PRIVILEGES ON DATABASE *database_name* TO *role_name*;
```

-  NPM зависимости: `npm install`
- `npx` пакет глобально: `npm install -g npx`
- создать папку "etc" в папке "dtpmap" и добавить туда три файла:
- secret_key.txt с секретным ключом для django
- database.txt с названием базы, логином и паролем через пробел

### Разработка
В дополнение к запуску сервера Django нужно запустить webpack `npm start` 
для генерации JavaScript кода.

### Запуск парсера данных со stat.gibdd.ru
Загрузить техническую информацию (названия разделов)
```
python3 parser.py tech_data
```

Загрузить регионы и районы
```
python3 parser.py regions
```

Загрузить данные по ДТП. Выгружаются только районы второго уровня (не крупные регионы, а по районам), у которых в базе стоит status = True. Таким образом можно выгружать только то, что вам нужно. По дефолту status = True у всех районов. 
```
python3 parser.py data
```

### Развертывание
Запустите эту команду перед развертыванием для генерации JavaScript кода:
```
npm run build-production
```
