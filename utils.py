import sys
import os


def auto_str(cls) -> object:
    def __str__(self):
        exclude_attrs = ['_AUTO_STR_EXCLUDE', '_AUTO_STR_SHOW_PRIVATE']
        if hasattr(self, '_AUTO_STR_EXCLUDE'):
            exclude_attrs += self._AUTO_STR_EXCLUDE
        show_private = False
        if hasattr(self, '_AUTO_STR_SHOW_PRIVATE') and self._AUTO_STR_SHOW_PRIVATE == True:
            show_private = True

        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items() if
                      (item[0] not in exclude_attrs) and (show_private or not item[0].startswith('_')))
        )

    cls.__str__ = __str__
    return cls


def boolean(s: str) -> bool:
    return s in ['true', 'True', 'TRUE', '1']


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_directory_if_not_exists(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)


def file_exists(file: str) -> bool:
    return os.path.isfile(file) and os.path.exists(file)


def absolute_path(relative_path: str) -> str:
    return os.path.abspath(relative_path)


def basename(filename: str) -> str:
    return os.path.basename(filename)


def get_env(name: str, default=None):
    r = os.getenv(name)
    if r is None:
        return default
    return r
