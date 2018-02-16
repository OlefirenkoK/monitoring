from celery import Celery
from molly.conf import settings


class UndefinedApplicationError(Exception):
    pass


def _get_repo_config(cfg, repo_name, field=None):
    repo_cfg = getattr(cfg, repo_name)
    if field is not None:
        return repo_cfg[field]
    else:
        return repo_cfg


def get_repo_config(repo_name, field=None, app=None):
    if app is None:
        return _get_repo_config(settings, repo_name, field=field)
    elif isinstance(app, Celery):
        return _get_repo_config(app.conf.cfg_backend, repo_name, field=field)
    else:
        raise UndefinedApplicationError
