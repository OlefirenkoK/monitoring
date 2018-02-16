from __future__ import absolute_import, unicode_literals

import logging
from datetime import timedelta

from celery.decorators import periodic_task

from rkn.task_queue.app import app
from rkn.utils.helper import get_repo_config
from rkn.repository.manager import RepositoryManager
from rkn.repository.repository import RepositoryFactory


logger = logging.getLogger(__name__)


def update_repo(repo_cfg):
    factory = RepositoryFactory()
    manager = RepositoryManager(factory, repo_cfg)
    manager.load()


@periodic_task(run_every=timedelta(seconds=get_repo_config('mirrors', 'repo_timeout', app=app)))
def periodic_update_mirrors_repo():
    logger.info('periodic_update_mirrors_repo')
    repo_cfg = get_repo_config('mirrors', app=app)
    update_repo(repo_cfg)


@periodic_task(run_every=timedelta(seconds=get_repo_config('rkn', 'repo_timeout', app=app)))
def periodic_update_rkn_repo():
    logger.info('periodic_update_rkn_repo')
    repo_cfg = get_repo_config('rkn', app=app)
    update_repo(repo_cfg)


@app.task
def mandatory_update_rkn_repo():
    logging.info('mandatory_update_rkn_repo')
    repo_cfg = get_repo_config('rkn')
    update_repo(repo_cfg)


@app.task
def mandatory_update_mirrors_repo():
    logging.info('mandatory_update_mirrors_repo')
    repo_cfg = get_repo_config('mirrors')
    update_repo(repo_cfg)
