# convert.py
import base64
from pathlib import Path

def convertFileToBase64(fileName: str) -> str:
    """Convert png file to base 64

    Parameters
    ----------
    fileName : str
        File path

    Returns
    -------
    str
        Base 64 encoding of png
    """
    with open(fileName, 'rb') as image:
        content = image.read()
        encoded = base64.b64encode(content)

    return encoded


# based on https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python

# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dirPath: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dirPath.iterdir())
    dirs = sorted([path for path in contents if path.is_dir()])
    files = sorted([path for path in contents if not path.is_dir()])
    contents = files + dirs
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if path.is_dir():
            yield prefix + pointer + path.name + '/'
        else:
            yield prefix + pointer + path.name
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)