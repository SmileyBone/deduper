import hashedfile
import sys
import io
import os
import time

def processFiles(folder):
    """given a starting folder process all of the data in the folder into a 
    dict of files keyed on the file hashes. This makes finding dupes with more than
    one value faster"""
    d = dict() #key = hash, data = list of hashedfile

    trail = os.walk(folder)
    
    for tri in trail:
        dir = tri[0]
        files = tri[2]

        for f in files:
            path = os.path.join(dir, f)
            hf = hashedfile.hashedfile(path)
            if hf.hashVal in d:
                others = d[hf.hashVal]
                others.append(hf)
                d[hf.hashVal] = others
            else:
                d[hf.hashVal] = [hf]
    return d
            

def filterlist(items):
    """given a list of items return either an empty list or a list of lists of duplicates"""
    returnlist = []
    list = items

    while len(list) > 0:
        checkItem = list.pop()
        dlist = [checkItem]
        newlist = []
        for i in list:
            if checkItem.deep_eq(i):
                dlist.append(i)
            else:
                newlist.append(i)
        list = newlist
        if len(dlist) > 1:
            returnlist.append(dlist)

    return returnlist


def dictGetDupes(dictoffiles):
    """given a dict of lists of file objects keyed on their hash,
        find the duplicates and return a list of lists"""
    dupes = []
    allItems = dictoffiles.itervalues()
    for items in allItems:
        if len(items) > 1:
            fItems = filterlist(items)
            if len(fItems) > 0:
                dupes.extend(fItems)

    return dupes



def getFilepathList(folder):
    """given a path to a folder find all of the files it containes
    and return a list of the path names."""

    filepaths = []
    
    trail = os.walk(folder)
    for tripple in trail:
        dir = tripple[0]
        files = tripple[2]

        for f in files:
            filepaths.append(os.path.join(dir, f))

    return filepaths

def getdupes(hl):
    """sort the list and then return a list of all possible dupes"""
    d = []

    hl.sort() #sort the list so that function is O(n*log(n)+n) vs O(n^2)

    hashcollisions = 0
    duplicates = 0

    for i in range(len(hl)-1):
        if hl[i].hashVal == hl[i+1].hashVal:
            hashcollisions += 1
            if hl[i].deep_eq(hl[i+1]):
                d.append((hl[i], hl[i+1]))
                duplicates += 1

    print "number of hash collisions: " + str(hashcollisions)
    print "number of duplicates: " + str(duplicates)

    return d


if __name__ == '__main__':
    
    path_is_valid = False
    while not path_is_valid:
        path = raw_input("Please enter the path to the folder to dedupe: ")
        if os.path.isdir(path):
           path_is_valid = True
        else: 
           print "please enter a valid directory path"
    
    start_time = time.time()
    filemap = processFiles(path)
    time_taken = time.time() - start_time
    print "files processed in " + str(time_taken)
    
    print "starting dupe search"
    start_time = time.time()
    dupes = dictGetDupes(filemap)
    time_taken = time.time() - start_time

    total = 0
    for list in dupes:
        total += (len(list))

    print str(total) + " dupes found in " + str(len(dupes)) + " sets in " + str(time_taken)
    
    raw_input("Press any key to print the duplicates.")
    print ""
    for list in dupes:
        for item in list:
            print item
        print ""
