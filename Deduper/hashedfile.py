import io
import ntpath
import hashlib

class hashedfile:
    """this file containes the filepath, hash, and any other useful
    data for a given file allong with the methods for creating and working with files."""
    
    def __init__(self, filepath):
        """given a filepath create and return a file object for that file.
            this does the hashing operation and is where the data is saved."""
        
        self.filepath = filepath
        
        with io.open(filepath, 'rb') as file:
            data = file.read(4096)

        self.hashVal = hashlib.md5(data).hexdigest()

    def __str__(self):
        return self.filepath

    def __lt__(self, other):
        return self.hashVal < other.hashVal

    def __eq__(self, other):
        return self.hashVal == other.hashVal

    def __ne__(self, other):
        return not self.__eq__(self, other)

    def deep_eq(self, other):
        with io.open(self.filepath, 'rb') as file:
            selfdata = file.read()
        with io.open(other.filepath, 'rb') as file:
            otherdata = file.read()
            
        return selfdata == otherdata