"""The Unix filesystem

https://en.wikipedia.org/wiki/Unix_filesystem#Conventional_directory_layout

The filesystem appears as one rooted tree of directories

Instead of addressing separate volumes such as disk partitions,
    removable media,
    and network shares as separate trees (
        as done in DOS and Windows:
            each drive has a LETTER naming the root of its file system tree),
    such volumes can be mounted on a directory,
    causing the volume's tree to appear as that directory in the larger tree
    The root of the entire tree is denoted.
"""

from pysyte.config.types import ModuleConfiguration
from pysyte.types.paths import path
from pysyte.types.paths import DirectPath


class UnixDirectory(DirectPath):
    def __init__(self, path_, sub_dirs=None):
        super().__init__(path_)
        for sub in sub_dirs or []:
            setattr(self, sub, self / sub)


root = path('/')
config = ModuleConfiguration(__file__)


def upath(string):
    """For consistency with path()"""
    return UnixDirectory(string)
