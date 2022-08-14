# Микросервис для скачивания файлов

Микросервис помогает работе основного сайта, сделанного на CMS и обслуживает
запросы на скачивание архивов с файлами. Микросервис не умеет ничего, кроме упаковки файлов
в архив. Закачиваются файлы на сервер через FTP или админку CMS.

Создание архива происходит на лету по запросу от пользователя. Архив не сохраняется на диске, вместо этого по мере упаковки он сразу отправляется пользователю на скачивание.

От неавторизованного доступа архив защищен хешом в адресе ссылки на скачивание, например: `http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/`. Хеш задается названием каталога с файлами, выглядит структура каталога так:

```
- photos
    - 3bea29ccabbbf64bdebcc055319c5745
      - 1.jpg
      - 2.jpg
      - 3.jpg
    - af1ad8c76fda2e48ea9aed2937e972ea
      - 1.jpg
      - 2.jpg
```


## Установка

Для работы микросервиса нужен Python версии не ниже 3.6.

```bash
pip install -r requirements.txt && apt install zip
```

## Запуск
```bash
python server.py
```

## Запуск с флагами hostname, port
```bash
python server.py -H 127.0.0.1 -P 7777
```

Сервер запустится на порту 7777 чтобы проверить его работу перейдите в браузере на страницу [http://127.0.0.1:7777/](http://127.0.0.1:7777/).

## Start on remote server with docker compose

Create **.env** file and set the <ins>following environmental variables</ins>:  
| Environmental          | Description                                       |
|------------------------|---------------------------------------------------|
| `ENABLE_RESPONSE_DELAY`| add delay for response when download zip file     |       
| `ENABLE_LOGGING`       | add logging to microservice                       |      
| `RESPONSE_DELAY`       | amount of delay for response                      |
| `PHOTOS_DIR`           | directory, where server keeps photos              |

Create **.docker_env** file for docker compose and set the <ins>following environmental variables</ins>:
| Environmental| Description                                       |
|--------------|---------------------------------------------------|
| `PORT`       | 4 digits port number for microservice             | 

Run with a docker compose with the following command:

```bash
 docker compose --env-file .docker_env up -d
 ```

After that, redirect requests to the microservice, starts with `/archive/`. For example:

```
GET http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/
GET http://host.ru/archive/af1ad8c76fda2e48ea9aed2937e972ea/
```
