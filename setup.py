import os

from setuptools import setup, find_packages


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


extras_require = {}

setup(
    name="rkn",
    version="0.0.1",
    description=("Monitoring"),
    classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Topic :: Internet :: WWW/HTTP'],
    author="__flash__",
    author_email="ne.peshite@suda.com",
    url="pornhub.com",
    license="proprietary",
    packages=find_packages(),
    install_requires=read("requirements.txt"),
    include_package_data=True,
    extras_require=extras_require,

    entry_points={
      "console_scripts": [
          "monitoring-server = rkn.server.start:main",
        ]
      }
)
