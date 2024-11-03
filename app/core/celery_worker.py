from celery import Celery
from flask import Flask

def make_celery(app: Flask) -> Celery:
    
    from app.tasks.external_jobs_task import log_task
    from app.tasks.notification_task import notify_user
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY'].broker_url,
        backend=app.config['CELERY'].result_backend
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    
    celery.conf.beat_schedule = app.config['CELERY'].beat_schedule
    
    return celery