import os
import json

from rkn.repository.repository import RepositoryFactory
from rkn.exceptions import RepositoryIsNotExistsError


class RepositoryManager:
    def __init__(self, factory=None, cfg=None):
        self._factory = factory  # type: RepositoryFactory
        self._cfg = cfg

    @property
    def cfg(self):
        return self._cfg

    @cfg.setter
    def cfg(self, cfg):
        self._cfg = cfg

    def get_repo(self):
        return self._factory.get_repository(self.cfg)

    def init(self):
        repo = self._factory.get_repository(self.cfg)
        repo.init()

    def update(self):
        repo = self._factory.get_repository(self.cfg)
        repo.update()

    def load(self):
        repo = self._factory.get_repository(self._cfg)
        if repo.created:
            repo.update()
        else:
            repo.init()


class MirrorRepositoryManager(RepositoryManager):
    MIRRORS_MAIN_FIELDS = ('mirror', 'master', 'mirrors')

    async def get_mirrors_info(self):
        repo = self.get_repo()
        if not repo.created:
            raise RepositoryIsNotExistsError

        mirrors_path = os.path.join(self.cfg.repo_path, self.cfg.mirrors_path)
        with open(mirrors_path) as f:
            mirrors_info = json.load(f)

        return mirrors_info

    async def get_mirrors_main_info(self):
        mirrors_info = await self.get_mirrors_info()
        return {field: mirrors_info[field] for field in self.MIRRORS_MAIN_FIELDS}


class RknRepositoryManager(RepositoryManager):
    pass
