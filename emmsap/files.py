# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from __future__ import print_function
import os
import music21
environLocal = music21.environment.Environment()

emmsapBase =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
emmsapDir = os.path.join(emmsapBase, 'xmldata')

try:
    unicode # @UndefinedVariable
except:
    unicode = str
    
def fixFilesInADir(dirName = emmsapDir):
    '''
    Rename all files in a directory that do not fit the naming scheme.
        
    :type dirName: str
    '''
    #: :type fn: str
    for fn in os.listdir(dirName): 
        newName = music21.common.normalizeFilename(fn) # @UndefinedVariable
        if newName.startswith('PMFC0'):
            newName = 'PMFC_0' + newName[5:]
            
        if fn != newName:
            print(fn, newName)
            os.rename(dirName + os.sep + fn, dirName + os.sep + newName)
            #return
            #exit()
            

def problemFileNames(filenameList):
    '''
    returns a list of tuples of problem filenames and suggested replacements
    
    >>> import emmsap.files
    >>> import pprint
    >>> allF = emmsap.files.allFiles()
    >>> pprint.pprint(emmsap.files.problemFileNames(allF))

    :type filenameList: list(str)
    '''
    import unicodedata  # @UnresolvedImport
    #from unidecode import unidecode as un # @UnresolvedImport
    returnList = []
    for fn in filenameList:
        fnNewer = unicodedata.normalize('NFC', unicode(fn))
        #fnNewer = un(fnNewer)
        fnNewList = []
        for n in fnNewer:
            if n.isalnum() or n == '_' or n == '.' or n == '-':
                fnNewList.append(n)
            else:
                fnNewList.append('_')
        fnNewer = ''.join(fnNewList)
        if fnNewer != fn:
            returnList.append( (fn, fnNewer),)
    return returnList

def allFiles():
    '''
    returns a list of all the files in the emmsapDirectory
    
    >>> import emmsap.files
    >>> af = emmsap.files.allFiles()
    >>> af[0:2]
    ['Amsterdam_64_Blijfs_mi_doch.xml', 'Arras_941_39v_si_vous_plait_tenor.xml']    
    >>> len(af)
    1739
    '''
    allFiles = os.listdir(emmsapDir)
    allFiles2 = []
    for f in allFiles:
        if f.startswith('.'):
            continue
        allFiles2.append(f)
    return allFiles2

def allFilesWithPath():
    '''
    returns a list of all the files in the emmsapDirectory
    with the full filepath
    
    >>> import emmsap.files    
    >>> afp = emmsap.files.allFilesWithPath()
    >>> afp[0]
    '/Users/Cuthbert/Dropbox/EMMSAP/MusicXML In/Amsterdam_64_Blijfs_mi_doch.xml'
    '''
    allFilesList = allFiles()
    allFilesPath = []
    for fn in allFilesList:
        allFilesPath.append(os.path.join(emmsapDir, fn))
    return allFilesPath

class FileIterator(object):
    '''
    iterate over the parsed version of all files
    
    >>> import emmsap.files
    >>> for n in emmsap.files.FileIterator():
    ...    p = n.parts[0]
    ...    m = p.measure(1)
    ...    m.show('text')
    ...    break
    {0.0} <music21.layout.PageLayout>
    {0.0} <music21.layout.SystemLayout>
    {0.0} <music21.clef.Treble8vbClef>
    {0.0} <music21.key.KeySignature of 1 flat, mode major>
    {0.0} <music21.meter.TimeSignature 2/4>
    {0.0} <music21.note.Note F>
    '''
    def __init__(self):
        self.data = allFilesWithPath()
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        post = self.data[self.index]
        self.index += 1
        try:
            x = music21.converter.parse(post) # @UndefinedVariable
            return x
        except Exception as e:
            environLocal.warn("ERROR on " + post + ": " + str(e))
            return next(self)

    def next(self):
        return self.__next__()

#------------------------------
if __name__ == '__main__':
    #problemFileNames()
    #fixFilesInADir('/Users/cuthbert/Dropbox/Jennings_Notation/Complete Notation Files')
    music21.mainTest()
