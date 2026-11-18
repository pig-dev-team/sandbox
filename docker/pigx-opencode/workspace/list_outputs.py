import json
import os
import stat
import sys

root, run, manifest = sys.argv[1:]
flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
paths = []
fd = os.open(root, flags)
try:
    for name in ('outputs', run):
        child = os.open(name, flags, dir_fd=fd)
        os.close(fd)
        fd = child
    for parent, dirs, files, directory in os.fwalk('.', dir_fd=fd, follow_symlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for name in files:
            if not name.startswith('.') and stat.S_ISREG(os.stat(name, dir_fd=directory, follow_symlinks=False).st_mode):
                paths.append(os.path.relpath(os.path.join(parent, name), '.'))
except FileNotFoundError:
    pass
finally:
    os.close(fd)
with open(manifest, 'x', encoding='utf-8') as f:
    json.dump(paths, f)
