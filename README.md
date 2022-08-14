# Microservice for downloading files asynchronously

Microservice helps the work of the main site made on CMS and serves
requests to download archives with files. Microservice can do nothing but pack files
to the archive. Files are uploaded to the server via FTP or CMS admin panel.

The creation of the archive occurs on the fly at the request of the user. The archive is not stored on disk; instead, as it is packaged, it is immediately sent to the user for download.

The archive is protected from unauthorized access by a hash in the download link address, for example: `http://host.ru/archive/3bea29ccabbbf64bdebcc055319c5745/`. The hash is given by the name of the directory with files, the directory structure looks like this:

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


## Setup
The microservice requires a Python version at least 3.6.

```bash
pip install -r requirements.txt && apt install zip
```

## Running
```bash
python server.py
```

## Running with flags hostname, port
```bash
python server.py -H 127.0.0.1 -P 7777
```

The server will start on port 7777 to check it go to the page in the browser [http://127.0.0.1:7777/](http://127.0.0.1:7777/).

## Start on a remote server with docker compose.

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
