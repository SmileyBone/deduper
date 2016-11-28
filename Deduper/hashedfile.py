import io
import ntpath
import hashlib
import os

class hashedfile:
    """this file containes the filepath, hash, and any other useful
    data for a given file along with the methods for creating and working with files."""
    BUFSIZE = 4*1024

    def __init__(self, filepath):
        """given a filepath create and return a file object for that file.
            this does the hashing operation and is where the data is saved."""

        self.filepath = filepath
        self.filesize = os.path.getsize(filepath)
        self.hashVal = self.filesize

    def __str__(self):
        return self.filepath

    def __lt__(self, other):
        return self.hashVal < other.hashVal

    def __eq__(self, other):
        return self.hashVal == other.hashVal

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def calc_hash(self):
        with io.open(filepath, 'rb') as file:
            data = file.read(self.BUFSIZE)

        self.hashVal = hashlib.md5(data).hexdigest()

    def deep_eq(self, other):
        result = False

        if self.filesize == other.filesize:
            with io.open(self.filepath, 'rb') as file1, io.open(other.filepath, 'rb') as file2:
                done = False
                while not done:
                    b1 = file1.read(self.BUFSIZE)
                    b2 = file2.read(self.BUFSIZE)

                    if b1 != b2:#we found a delta in the files
                        done = True

                    if not b1 and not b2: #we hit the end of the files
                        result = True
                        done = True
        return result
