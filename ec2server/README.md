## How to Run

### Run RabbitMQ

```bash
docker run --name rabbitmq -p 5672:5672 rabbitmq:3
```

### Run Celery

```bash
celery -A watcher worker --app=watcher -l info
```

### Run Django Web Server

```bash
python manage.py runserver
```

## Debug

### Check Task Progress

```bash
python check_celery.py <task_id>
```
