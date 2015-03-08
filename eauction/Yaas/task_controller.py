__author__ = 'eyob'

import django
from celery.task import periodic_task
from celery.schedules import crontab
from Yaas import tasks
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta

django.setup()
logger = get_task_logger(__name__)

@periodic_task(run_every =crontab(hour='*', minute='*',day_of_week='*'))
def tasks_todo():

    logger.info("Start task")
    tasks.do_task()
    logger.info("Task finished!")