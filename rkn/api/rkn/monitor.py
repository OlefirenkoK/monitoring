import logging

from aiohttp.web import json_response, Request
from molly.conf import settings

from rkn.task_queue.tasks.rkn import mandatory_update_rkn_repo
from rkn.repository.manager import MirrorRepositoryManager, RknRepositoryManager
from rkn.repository.repository import RepositoryFactory
from rkn.utils.helper import get_repo_config


logger = logging.getLogger(__name__)


class Monitor:
    async def status(self, _):
        import os
        from rkn.utils.csv_reader import main
        from rkn.repository.manager import RepositoryManager
        from rkn.repository.repository import RepositoryFactory

        # URL_BOARDER = 'https://github.com/OlefirenkoK/Border.git'
        # REPO_PTH = os.path.join('/tmp/', 'boarder_repo')

        # from rkn.utils.helper import get_repo_config
        # cfg = get_repo_config('rkn')
        #
        # factory = RepositoryFactory()
        # repo = factory.get_repository(cfg)
        # logger.info('prepre')
        # repo.update()
        # logger.info('done')

        # main()
        # update_rkn_repo(settings.repo_url, settings.repo_path)

        return json_response({'result': True})

    async def update(self, _):
        mandatory_update_rkn_repo.delay()
        return json_response({'result': True})
    
    async def get_mirrors(self, _):
        repo_cfg = get_repo_config('mirrors')
        manager = MirrorRepositoryManager(RepositoryFactory(), cfg=repo_cfg)
        mirrors_info = await manager.get_mirrors_info()
        return json_response({'result': mirrors_info})
