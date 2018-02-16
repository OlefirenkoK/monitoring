from rkn.api.rkn.monitor import Monitor


monitor = Monitor()


handlers = [
    ('get', '/api/3/rkn/status', monitor.status),
    ('get', '/api/3/rkn/update', monitor.update),
    ('get', '/api/3/rkn/get_mirrors', monitor.get_mirrors),
]
