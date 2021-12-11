from celery import Celery

celery_app = Celery(__name__, broker="redis://redis:6379/0")

celery_app.autodiscover_tasks(packages=['celery_app'])

celery_app.conf.task_routes = {"celery_app.tasks.*": "main-queue"}
