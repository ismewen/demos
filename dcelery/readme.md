### about
django有个扩展，`django-celery-beat`, 可以把`schedule` 存储在数据库中。通过数据库来进行任务调度。个人觉得十分好用，所以决定把它抄到flask中，
也就有了这个demo。

### quick start 

#### 配置
通过CELERYBEAT_SCHEDULE这个参数配置调度方式，初次加载的时候，会将其写入到数据库中，不过请注意如下两点
 - **数据库中的任务拥有最高优先级** 如果数据库中已经存在了该task，这里的配置不会覆盖数据库中的task
 - 所有的时间都为utc时间

```python
CELERYBEAT_SCHEDULE = {
    "say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": crontab(minute="*/1", hour=arrow.utcnow().hour)
    },
    "interval_say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": 3*10,
    },
    "clocked_say_hello": {
        "task": "modules.routines.tasks.say_hello",
        "schedule": clocked(clocked_time=arrow.utcnow().shift(minutes=3).datetime, enabled=True),
    }
}
```


#### 启动命令

celery -A celery_app.celery_app beat -l debug --scheduler modules.routines.schedulers.DatabaseScheduler


