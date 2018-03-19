import logging
from os.path import abspath, join, dirname
from os import pardir

_ROOT = abspath(
    join(
        dirname(abspath(__file__)),
        pardir
    )
)
# SCRAPER_LOG = join(_ROOT, "db", "log.json")

LOGGING_LEVEL = "INFO"


log = logging
log.basicConfig()  # format='%(asctime)s %(message)s')
log.getLogger().setLevel(LOGGING_LEVEL)
