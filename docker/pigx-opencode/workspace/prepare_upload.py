import os
import stat
import sys

root = sys.argv[1]
for target in sys.argv[2:]:
    parent = root
    for part in os.path.relpath(os.path.dirname(target), root).split('/'):
        parent = os.path.join(parent, part)
        try:
            os.mkdir(parent, 0o700)
        except FileExistsError:
            pass
        if not stat.S_ISDIR(os.lstat(parent).st_mode):
            raise ValueError('invalid directory')
    fd = os.open(target, os.O_CREAT | os.O_TRUNC | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    os.fchmod(fd, 0o600)
    os.close(fd)
