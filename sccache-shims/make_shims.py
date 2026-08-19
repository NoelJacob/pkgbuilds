from os import environ, listdir, remove, symlink
from pathlib import Path
from re import compile
from sys import argv


def main():
    b = argv[1]
    if len(argv) != 2:
        raise Exception("Invalid invocation")
    path = environ.get("PATH")
    regex = compile(
        r'^(?:(?:.*-)?(gnu-|musl-|eabi-|mingw-|android-))?'
        r'(gcc|g\+\+|clang|clang\+\+|cc|c\+\+|cl|rustc)'
        r'(-[0-9.]+)?$'
    )
    if path is None:
        raise Exception("Path is unavailabe")
    path_list = path.split(":")
    if "/usr/lib/sccache-shims/bin" in path_list:
        path_list.remove("/usr/lib/sccache-shims/bin")
    a = {}
    for x in path_list:
        dir_path = Path(x)
        if dir_path.exists():
            for y in listdir(dir_path):
                z = dir_path.joinpath(y)
                if z.exists() and (z.stat().st_mode & 0o111) and (z.stem not in a) and regex.match(z.stem):
                    a[z.stem] = z.absolute().as_posix()
    for (c, d) in a.items():
        e = Path(b).joinpath(c)
        if e.exists():
            remove(e)
        symlink(d, e)

if __name__ == "__main__":
    main()
