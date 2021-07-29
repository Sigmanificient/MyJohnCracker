""" archive is an simple python script to compare multiple hash with a dictionary of word """
# python ~= 3.9

from time import perf_counter
from hashlib import sha256

from os import listdir, path
from sys import argv
from typing import Optional, List

__version__: str = "1.0"
__author__: str = "Yohann Boniface"


class Main:
    """
       ______  ______      ____              __
      / ____ \\/ ____/_  __/ / /_  ___  _____/ /_
     / / __ `/ /_  / / / / / __ \\/ _ \\/ ___/ __/
    / / /_/ / __/ / /_/ / / /_/ /  __/ /  / /_
    \\ \\__,_/_/    \\__,_/_/_.___/\\___/_/   \\__/
     \\____/ __           __        ___                  __
       / / / /___ ______/ /__     /   | _________ _____/ /__  ____ ___  __  __
      / /_/ / __ `/ ___/ //_/    / /| |/ ___/ __ `/ __  / _ \\/ __ `__ \\/ / / /
     / __  / /_/ / /__/ ,<      / ___ / /__/ /_/ / /_/ /  __/ / / / / / /_/ /
    /_/ /_/\\__,_/\\___/_/|_|    /_/  |_\\___/\\__,_/\\__,_/\\___/_/ /_/ /_/\\__, /
                                                                     /____/"""

    def __init__(self, all_hash: str = "assets/hash", dictionary: str = "assets/dict", *overflow: str):
        print(self.__doc__)
        if overflow or '--help' in argv:
            print(self)
            return

        self.all_hash: List[str] = self.get_content(all_hash)
        self.dictionary: List[str] = self.get_content(dictionary)
        print(' results '.center(32, '-'))

        self.multiple(self.all_hash) if len(self.all_hash) != 1 else self.single(self.all_hash[0])
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
        """ Warning HL101: MD5, SHA-1, RIPEMD-160, Whirlpool, and the SHA-256 / SHA-512 hash algorithms are all
        vulnerable to length-extension attacks and should not be used for obfuscating or protecting data. Use within
        a HMAC is not vulnerable. ( Hashlib Documentation )"""
        return sha256(string.encode()).hexdigest()

    def single(self, _hash: str):
        """ When only one hash is provided, scroll directly within the directory """

        val: str
        for val in self.dictionary:
            if self.get_hash(val) == _hash:
                self.log(f"Found matching hash for {val} ({_hash})")
                break
        else:
            self.log("<!> No hash found")

    def multiple(self, _hash_list: List[str]):
        """ When hash file contains multiple lines or multiple files are given.
        An hash dictionary is built which is way faster than a multiple for loop but ask lots of memory """
        self.dictionary: dict[str:str] = {self.get_hash(val): val for val in self.dictionary}

        _hash: str
        for _hash in _hash_list:
            val: Optional[str] = self.dictionary.get(_hash)
            self.log("<!> No hash found" if val is None else f"Found matching hash for {val} ({_hash})")

    @staticmethod
    def log(string: str):
        """ print with an time marker """
        print(f"[{perf_counter():,.3f}s] {string}")

    def get_content(self, _path: str) -> List[str]:
        """ Get all values from a path and merge file if a directory is given """
        if path.isfile(_path):
            print(f"Opening file: {_path}")
            with open(_path) as f:
                return f.read().splitlines()

        elif path.isdir(_path):
            files: List[List[str]] = []
            print(f"Opening folder: {_path}")

            filename: str
            for filename in listdir(_path):
                if not filename.endswith('.txt'):
                    continue

                print(f"+ {filename}")

                with open(f"{_path}/{filename}") as f:
                    files.append(f.read().splitlines())

            return [line for file in files for line in file]

        print("File or Directory not found !", self)
        quit()


if __name__ == '__main__':
    Main(*argv[1:])
