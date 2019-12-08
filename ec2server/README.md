### Run RabbitMQ

```bash
docker run --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3
```

### Run Celery

```bash
celery -A watcher worker --app=watcher -l info
```
