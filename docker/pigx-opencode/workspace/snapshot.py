import os
import stat
import sys

root, path, staging, limit = sys.argv[1:]
limit = int(limit)
parts = path.split('/')
# O_NOFOLLOW rejects symlinks but still allows '..' to open a parent directory.
if os.path.isabs(path) or '..' in parts:
    raise ValueError('path must stay inside outputs')
fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
try:
    for part in ['outputs'] + parts[:-1]:
        next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
        os.close(fd)
        fd = next_fd
    source = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
    with os.fdopen(source, 'rb') as src:
        info = os.fstat(src.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError('invalid file or size')
        os.mkdir(staging, 0o700)
        with open(staging + '/file', 'xb') as dst:
            count = 0
            while chunk := src.read(65536):
                count += len(chunk)
                if count > limit:
                    raise ValueError('file too large')
                dst.write(chunk)
finally:
    os.close(fd)
