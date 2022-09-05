**Информационный сервис о проезде транспортного средства**

Шаблон проекта от https://github.com/anthonycepeda/fastapi-mongodb-async-restapi

Инструкция по запуску:

1. Собрать базовый контейнер с зависимостями
```bash
docker build -f DockerfileBase -t fastapi-traffic:base .
```
2. Собрать контейнер с исходниками
```bash
docker build -t fastapi-traffic .
```
3. Запустить сервис
```bash
docker-compose up --force-recreate
```

Посетить [сваггер](localhost:4666/traffic-info/swagger) (localhost:4666/traffic-info/swagger) для получения информации по запросам

