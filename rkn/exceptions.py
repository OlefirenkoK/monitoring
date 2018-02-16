class RepositoryAlreadyExistsError(Exception):
    """Raise if repository already exists for given path"""


class RepositoryIsNotExistsError(Exception):
    """Raise if repository is not exists for given path"""
