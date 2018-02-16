import logging
import csv
import os
import re

from molly.conf import settings

from rkn.utils.constants import RKN_DUMP


IP_REGEX = re.compile(r'(\d{1,3})[.](\d{1,3})[.](\d{1,3})[.](\d{1,3})')
# DOMAIN_REGEX = re.compile(r'^(?P<subset>\*\.)?(?P<base>([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,})$')
DOMAIN_REGEX = re.compile(r'^(?P<subset>\*\.)?(?P<base>(\w+(-\w+)*\.)+\w{2,})$', re.IGNORECASE)


logger = logging.getLogger(__name__)


class IncorrectSchemaError(Exception):
    """Raise if given fields are incorrect"""


class RknAnalyzer:
    VALID_SCHEMA_LENGTH = 6

    @classmethod
    def analyze(cls, fields):
        try:
            ip_list, domain = cls._parse_normal_schema(fields)
        except IncorrectSchemaError:
            ip_list, domain = cls._parse_incorrect_schema(fields)

        return ip_list, domain

    @classmethod
    def _parse_normal_schema(cls, fields):
        if len(fields) != cls.VALID_SCHEMA_LENGTH:
            raise IncorrectSchemaError

        ip_list, domain = cls._serialization_to_ip_list(fields[0]), cls._serialization_to_domain(fields[1])
        return ip_list, domain

    @classmethod
    def _parse_incorrect_schema(cls, fields):
        if len(fields) == cls.VALID_SCHEMA_LENGTH - 1:
            ip_list, domain = None, cls._serialization_to_domain(fields[0])
        elif len(fields) > cls.VALID_SCHEMA_LENGTH:
            ip_list, domain = cls._serialization_to_ip_list(fields[0]), cls._serialization_to_domain(fields[1])
        else:
            ip_list, domain = None, None

        return ip_list, domain

    @staticmethod
    def _serialization_to_ip_list(field):
        ip_list = IP_REGEX.findall(field)
        return ip_list

    @staticmethod
    def _serialization_to_domain(field):
        match = DOMAIN_REGEX.match(field)
        if match:
            domain = match.groupdict().get('base')
        else:
            domain = None
        return domain


def is_blocked(mirrors, domain):
    raise NotImplementedError


def set_blocked(mirror):
    raise NotImplementedError


def check_blocked_mirrors(mirrors):
    dump_path = os.path.join(settings.repo_path, RKN_DUMP)

    with open(dump_path, encoding='ISO-8859-1') as f:
        parser = csv.reader(f, delimiter=';', quotechar='|')

    for fields in parser:
        _, domain = RknAnalyzer.analyze(fields)
        if is_blocked(mirrors, domain):
            set_blocked(domain)


def main():
    pass


if __name__ == '__main__':
    settings = type('Settings', (object, ), {'repo_path': '/tmp/z-i_repo'})
    RKN_DUMP = 'dump.csv'
    import time
    start = time.time()
    x = main()
    stop = time.time()
    print('Time: {} ||| x = {}'.format(stop - start, x))
