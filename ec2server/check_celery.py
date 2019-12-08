import sys
from celery import result, Celery

app = Celery('watcher', backend='amqp', broker='amqp://guest:guest@localhost//')
res = result.AsyncResult(id=sys.argv[1], app=app)
print(res.state)
print(res.info)
