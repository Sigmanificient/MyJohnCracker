"""
An python script to compare multiple hash with a dictionary of word.

:argument:
--help			Show this helpful message

:param[1]:		Hash path,	default: [assets/hash]
:param[2]:		Dictionary	path, default: [assets/dict]
"""
import os
from time import perf_counter
from hashlib import sha256

from os import listdir, path
from sys import argv
from typing import Optional, List, Dict

__version__: str = "1.0"
__author__: str = "Yohann Boniface"


class App:

    def __init__(
        self,
        all_hash: str = "assets/hash",
        dictionary: str = "assets/dict",
        *overflow: str
    ):
        """Initialize the application with given sys argy."""
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
        self.run()

    def __repr__(self):
        """Representation give the help message."""
        return '\n'.join((
            "archive - This is the help message.",
            "--help\t\t\tShow this helpful message", '',
            "@param[1]:\t\tHash path,\tdefault: [assets/hash]",
            "@param[2]:\t\tDictionary\tpath, default: [assets/dict]"
        ))

    def run(self):
        """Start the hash brute force process."""
        if len(self.all_hash) != 1:
            self.multiple(self.all_hash)

        else:
            self.single(self.all_hash[0])

        os.system("pause")

    def single(self, _hash: str) -> None:
        """Scroll within the dictionary until a hash matches."""
        for val in self.dictionary:
            if self.get_hash(val) == _hash:
                self.log(f"Found matching hash for {val} ({_hash})")
                break
        else:
            self.log("<!> No hash found")

    def multiple(self, _hash_list: List[str]) -> None:
        """Build a hash dictionary or proceed multiple hash lookup."""

        self.dictionary: Dict[str, str] = {
            self.get_hash(val): val for val in self.dictionary
        }

        for _hash in _hash_list:
            val: Optional[str] = self.dictionary.get(_hash)

            self.log(
                "<!> No hash found"
                if val is None else f"Found matching hash for {val} ({_hash})"
            )

    def get_content(self, _path: str) -> Optional[List[str]]:
        """Get the files contents of a given file or directory."""
        if path.isfile(_path):
            return self.read_single_file(_path)

        if path.isdir(_path):
            return self.read_folder_files(_path)

    @staticmethod
    def get_hash(string) -> str:
        """Return the sh256 hash of a string."""
        return sha256(string.encode()).hexdigest()

    @staticmethod
    def log(string: str) -> None:
        """Prints a formatted log with a time marker."""
        print(f"[{perf_counter():,.3f}s] {string}")

    @staticmethod
    def read_single_file(_path: str) -> List[str]:
        """Read lines from a given file path."""
        print(f"Opening file: {_path}")

        with open(_path) as f:
            return f.read().splitlines()

    @staticmethod
    def read_folder_files(_path: str) -> List[str]:
        """Read multiple files from a folder and merge there lines."""
        files: List[List[str]] = []
        print(f"Opening folder: {_path}")

        for filename in listdir(_path):
            if not filename.endswith('.txt'):
                continue

            print(f"+ {filename}")

            with open(f"{_path}/{filename}") as f:
                files.append(f.read().splitlines())

        return [line for file in files for line in file]


def print_ascii_art() -> None:
    """Prints the school ascci art in the console."""
    with open('assets/asciiart/asciiart.txt') as f:
        print(f.read())


if __name__ == '__main__':
    App(*argv[1:])
