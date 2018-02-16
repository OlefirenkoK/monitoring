from __future__ import absolute_import, unicode_literals

from celery import Celery
from molly.conf import settings

from rkn.utils.constants import BACKEND_CONFIG_PATH


app = Celery(
    main='task_queue',
    broker='amqp://',
    backend='amqp://',
    include=['rkn.task_queue.tasks.rkn'])


app.conf.update(
    result_expires=3600,
    cfg_backend=(lambda: settings.setup(BACKEND_CONFIG_PATH))()
)


if __name__ == '__main__':
    app.start()
