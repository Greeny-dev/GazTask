# Control Service 

Сервис реализующий управление теплицами. 

## Startup

```commandline
docker-compose up --build
```

## Configuration (Environments)

      DB_HOST: db_host
      DB_PORT: db_port
      DB_USER: db_user
      DB_PASS: db_password
      DB_NAME: db_name
      LOG_LEVEL: "INFO"/"CRITICAL"/"DEBUG"/"WARNING". "DEBUG" recomended. 
      LOG_FORMAT: "PLAIN"/"JSON"
      API_SERVER_HOST: api_server_host
      API_SERVER_PORT: api_server_port
      GREENHOUSE_SERVICE: greenhouse_service_url 
      ASSESSMENT_SERVICE: greenhouse_service_url 


## Updates 

Очевидно: для полноценной prod реализации не хватает следующих аспектов: 

- Написанных unit/интеграционных тестов. 
- Обработки ошибок (частично зависит от пункта 1). Пример можно встретить [здесь.](./src/infrastructure/greenhouses_service/errors.py)
- Грамотной системы логирования.

Их отсутствие связано с занятостью dev-а. Каждая из этих категорий будет реализована в последующих версиях. Следите за обновлением [api схемы](./api/openapi.json)

