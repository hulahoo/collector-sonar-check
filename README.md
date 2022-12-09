# events-collector

Сервис создан для импорта внешних ресурсов Threat Intelligence.

### Запуск воркера 

- Скопируйте данный репозиторий

Запустите локальный сервер (только для разработки, будет использована sqlite БД)

- dagit -f main.py появится веб интерфейс и по нему нужно будет перейти и запустить

* (config)

```yaml
ops:
  consumer_dispatcher_op:
    config:
      partitions: [ 1,2,3 ]
```

## Информаци о ENV-параметрах
Имеющиеся env-параметры в проекте:
    ```
    KAFKA_BOOTSTRAP_SERVER=""  # хост на котором расположена кафка
    KAFKA_GROUP_ID=""  # груп id кафки  
    TOPIC_CONSUME_EVENTS=""
    POSTGRES_SERVER=""
    POSTGRES_PASSWORD=""
    POSTGRES_USER=""
    POSTGRES_DB=""
    POSTGRES_PORT=""
    ```
  

## Информация о файлах конфигурации
Все конфигурции можно найти в директории:
```
  src/apps/config
```
