"""
An python script to compare multiple hash with a dictionary of word.

:argument:
--help			Show this helpful message

:param[1]:		Hash path,	default: [assets/hash]
:param[2]:		Dictionary	path, default: [assets/dict]
"""

from time import perf_counter
from hashlib import sha256

from os import listdir, path
from sys import argv
from typing import Optional, List, Dict

__version__: str = "1.0"
__author__: str = "Yohann Boniface"


class Main:

    def __init__(
        self,
        all_hash: str = "assets/hash",
        dictionary: str = "assets/dict",
        *overflow: str
    ):
        print_ascii_art()

        if overflow or '--help' in argv:
            print(self)
            return

        self.all_hash: List[str] = self.get_content(all_hash)
        self.dictionary: List[str] = self.get_content(dictionary)

        if self.all_hash is None or self.dictionary is None:
            print("File or Directory not found !", self)
            return

        print(' results '.center(32, '-'))

        if len(self.all_hash) != 1:
            self.multiple(self.all_hash)

        else:
            self.single(self.all_hash[0])

        input("Press enter key to quit...")

    def __repr__(self):
        """ Representation give an help message """
        return '\n'.join((
            "archive - This is the help message.",
            "--help\t\t\tShow this helpful message", '',
            "@param[1]:\t\tHash path,\tdefault: [assets/hash]",
            "@param[2]:\t\tDictionary\tpath, default: [assets/dict]"
        ))

    @staticmethod
    def get_hash(string) -> str:
        return sha256(string.encode()).hexdigest()

    def single(self, _hash: str) -> None:
        """If only one hash is provided, scroll within the directory."""
        for val in self.dictionary:
            if self.get_hash(val) == _hash:
                self.log(f"Found matching hash for {val} ({_hash})")
                break
        else:
            self.log("<!> No hash found")

    def multiple(self, _hash_list: List[str]) -> None:
        """When hash file contains multiple lines
            or multiple files are given.

        An hash dictionary is built which is way faster than a multiple
        for loop but ask lots of memory."""
        self.dictionary: Dict[str, str] = {
            self.get_hash(val): val for val in self.dictionary
        }

        for _hash in _hash_list:
            val: Optional[str] = self.dictionary.get(_hash)

            self.log(
                "<!> No hash found"
                if val is None else f"Found matching hash for {val} ({_hash})"
            )

    @staticmethod
    def log(string: str) -> None:
        """ print with an time marker """
        print(f"[{perf_counter():,.3f}s] {string}")

    @staticmethod
    def get_content(_path: str) -> Optional[List[str]]:
        """Get all values from path and merge file if a directory is
            given."""
        if path.isfile(_path):
            print(f"Opening file: {_path}")

            with open(_path) as f:
                return f.read().splitlines()

        if not path.isdir(_path):
            return

        files: List[List[str]] = []
        print(f"Opening folder: {_path}")

        for filename in listdir(_path):
            if not filename.endswith('.txt'):
                continue

            print(f"+ {filename}")

            with open(f"{_path}/{filename}") as f:
                files.append(f.read().splitlines())

        return [line for file in files for line in file]


def print_ascii_art():
    with open('assets/asciiart/asciiart.txt') as f:
        print(f.read())


if __name__ == '__main__':
    Main(*argv[1:])
