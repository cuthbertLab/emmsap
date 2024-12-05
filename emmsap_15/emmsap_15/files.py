import os
import music21
import pathlib
import unicodedata

environLocal = music21.environment.Environment()

emmsapBase = pathlib.Path(__file__).parent.parent
emmsapDir = emmsapBase / 'xml15data'


# def fixFilesInADir(dirName: pathlib.Path = emmsapDir):
#     '''
#     Rename all files in a directory that do not fit the naming scheme.
#     '''
#     for fn_bytes in sorted(os.listdir(dirName)):
#         fn = fn_bytes.decode('utf-8', errors='ignore')
#         newName = music21.common.normalizeFilename(fn)
#         if newName.startswith('PMFC0'):
#             newName = 'PMFC_0' + newName[5:]
#
#         if fn != newName:
#             print(fn, newName)
#             os.rename(dirName + os.sep + fn,
#                       dirName + os.sep + newName)
#             # return
#             # exit()


def problemFileNames(filenameList: list[str]):
    '''
    returns a list of tuples of problem filenames and suggested replacements

    >>> from emmsap_15.emmsap_15 import files
    >>> import pprint
    >>> allF = files.allFiles()
    >>> pprint.pprint(files.problemFileNames(allF))
    '''
    returnList = []
    for fn in filenameList:
        fnNewer = unicodedata.normalize('NFC', fn)
        # fnNewer = un(fnNewer)
        fnNewList = []
        for n in fnNewer:
            if n.isalnum() or n == '_' or n == '.' or n == '-':
                fnNewList.append(n)
            else:
                fnNewList.append('_')
        fnNewer = ''.join(fnNewList)
        if fnNewer != fn:
            returnList.append((fn, fnNewer),)
    return returnList


def allFiles() -> list[str]:
    '''
    returns a list of all the files in the emmsapDirectory

    >>> from emmsap_15.emmsap_15 import files
    >>> af = files.allFiles()
    >>> af[0:2]
    ['Amsterdam_64_Blijfs_mi_doch.xml', 'Arras_941_39v_si_vous_plait_tenor.xml']
    >>> len(af)
    1739
    '''
    all_files = emmsapDir.iterdir()
    allFiles2: list[str] = []
    for f in sorted(all_files):
        if f.name.startswith('.'):
            continue
        allFiles2.append(f.name)
    return allFiles2


def allFilesWithPath():
    '''
    returns a list of all the files in the emmsapDirectory
    with the full filepath

    >>> from emmsap_15.emmsap_15 import files
    >>> afp = files.allFilesWithPath()
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

    >>> from emmsap_15.emmsap_15 import files
    >>> for n in files.FileIterator():
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
            x = music21.converter.parse(post)
            return x
        except Exception as e:
            environLocal.warn("ERROR on " + post + ": " + str(e))
            return next(self)

    def next(self):
        return self.__next__()


class FourteenthCenturyIterator(FileIterator):
    '''
    An iterator that only includes well-edited 14th and early 15th c. pieces.
    '''
    # noinspection SpellCheckingInspection
    skips = '''
    Basel_Gaudet_Novum.xml
    Bodley 842 59v.xml
    Bodley_842_Ut_patet.xml
    Bologna_2216_Verbum_Caro_Incomplete.xml
    CMM79_1_02_039.xml
    CMM79_1_03_040.xml
    CMM79_1_04_043.xml
    CMM79_1_05_045.xml
    CMM79_1_06_047.xml
    CPDL_Magister_Andreas-Sanctus_Trent92_212v.xml
    Ciconia_Potential_Parody_Gloria.xml
    German_Basses_Auction_pt2.musicxml
    XXbDieMinneFugetWolkenstein65c.xml
    '''.splitlines()
    skips = [s.strip() for s in skips]

    def __init__(self):
        super().__init__()
        new_data = []
        for fn in self.data:
            reject = False
            fp = pathlib.Path(fn)
            for skip_start in ('mo_', 'ba_', 'OMF', 'OMR', 'FallowsMB'):
                if fp.name.startswith(skip_start):
                    reject = True
                if fp.name in self.skips:
                    reject = True
            if reject:
                continue
            new_data.append(fn)
        self.data = new_data


# ------------------------------
if __name__ == '__main__':
    music21.mainTest()
