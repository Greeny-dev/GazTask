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
