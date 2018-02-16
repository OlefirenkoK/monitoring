import os
import logging
from abc import ABCMeta, abstractmethod, abstractclassmethod, abstractproperty

import git

from rkn.exceptions import RepositoryAlreadyExistsError, RepositoryIsNotExistsError


logger = logging.getLogger(__name__)


class RepositoryInitError(Exception):
    def __init__(self, cfg):
        self._cfg = cfg

    def __str__(self):
        return 'Impossible to create repo with given parameters: {}'.format(self._cfg)


class AbstractRepository(metaclass=ABCMeta):
    @abstractproperty
    def created(self):
        """"""
        
    @abstractmethod
    def init(self):
        """"""
        
    @abstractmethod
    def update(self):
        """"""


class BaseRepository(AbstractRepository):
    REPO_FOLDER = None

    def __init__(self, repo_cfg):
        try:
            url, path, timeout = repo_cfg['repo_url'], repo_cfg['repo_path'], repo_cfg['repo_timeout']
        except (KeyError, ValueError, TypeError):
            raise RepositoryInitError(repo_cfg)

        self.url = url
        self.path = path
        self.timeout = timeout

    @property
    def created(self):
        return os.path.isdir(os.path.join(self.path, self.REPO_FOLDER))
    
    def init(self):
        if self.created:
            raise RepositoryAlreadyExistsError
    
    def update(self):
        if not self.created:
            raise RepositoryIsNotExistsError


class GitRepository(BaseRepository):
    REPO_FOLDER = '.git'

    @property
    def repo(self):
        return git.Repo(self.path)

    @property
    def remote(self):
        return self.repo.remote()

    def init(self, branch='master'):
        super().init()
        git.Repo.clone_from(self.url, self.path, branch=branch)
        logger.info("Repository (url: {}) created in {}".format(self.url, self.path))

    def update(self):
        super().update()
        self.remote.pull()
        self.remote.fetch()
        logger.info("Repository (url: {}) updated successfully in {}".format(self.url, self.path))


class RepositoryFactory:
    def get_repository(self, repo_cfg):
        klass = self._analyze_repo(repo_cfg)
        repo = klass(repo_cfg)
        return repo

    def _analyze_repo(self, cfg):
        """Currently just returns GitRepository"""
        return GitRepository
