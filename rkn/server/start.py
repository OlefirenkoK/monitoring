import sys
import asyncio

from molly import server

from rkn.server.handlers import handlers


def main():
    cfg_cmd = server.options.parse_command_line(sys.argv[1:])
    server.logger.setup(cfg_cmd.logging)
    cfg = server.conf.setup(cfg_cmd)
    loop = asyncio.get_event_loop()

    application = server.make_application(loop, cfg, handlers)
    server.start(loop, application, cfg)
