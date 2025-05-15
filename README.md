# Oscar Studio. Тестовое задание

## Описание:
Микросервис рассылки. Содержит один эндпоинт для отправки сообщения.
Реализована возможность отправки в ТГ и на почту. 
В поле получателей можно передать как одного пользователя, так и список.
В зависимости от параметра delay происходит моментальная отправка 
или отправка с задержкой (в 1 час или в 1 день).

**Примечание**: относительно ТЗ исправлена опечатка в названии поля:
`recepient` заменено на `recipient`.

## Доступ:
API развернуто на сервере по адресу:
```
http://193.164.150.86:8097/api/swagger/
```
Для того, чтобы пользователь начал получать сообщения в ТГ, 
нужно активировать бота `t.me/AKolmychekBot` через команду `\start`



## Запуск проекта через docker:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Anna-Kolmychek/oscar_studio.git
```
ИЛИ
```
git clone https://github.com/Anna-Kolmychek/oscar_studio.git
```
И
```
cd oscar_studio
```

Создать и заполнить .env по образцу .env_template:
```
mv .env_template .env
nano .env
```

Собрать и запустить контейнеры:
```
docker compose up -d --build
```

После запуска сервера документация к API будет доступна по ссылке:  
http://127.0.0.1:8097/api/swagger/

Админка будет доступна по ссылке:  
http://127.0.0.1:8097/admin/


## Локальный запуск проекта без сборки образов:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Anna-Kolmychek/oscar_studio.git
```
ИЛИ
```
git clone https://github.com/Anna-Kolmychek/oscar_studio.git
```
И
```
cd oscar_studio
```

Создать и активировать виртуальное окружение:
```
python -m venv venv
```
```
venv\Scripts\activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Создать и заполнить .env по образцу .env_template:
```
mv .env_template .env
nano .env
```

Выполнить миграции
```
python manage.py makemigrations
python manage.py migrate
```

Запустить локальный сервер Django:
```
python manage.py runserver
```
и celery (должен быть установлен и запущен redis):
```
celery -A config worker --loglevel=info
```

После запуска сервера документация к API и примеры запросов будут доступны по ссылкам:
http://127.0.0.1:8000/api/redoc/ и http://127.0.0.1:8000/api/swagger/

Админка доступна по ссылке
http://127.0.0.1:8000/admin/
