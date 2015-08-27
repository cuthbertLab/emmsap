# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
Methods related to reconciling the spreadsheet with the directory.
'''


from emmsap import files
from emmsap import spreadsheet
import music21    

def inSheetNotInDir():
    '''
    returns a list of files that seem to exist in the
    spreadsheet but are not in the directory.
    
    >>> import emmsap.fileAndSheet
    >>> isnid = emmsap.fileAndSheet.inSheetNotInDir()
    >>> isnid
    []
    >>> len(isnid)
    23
    '''
    allSheetNames = spreadsheet.Workbook().allFilenames()
    allDirNames = files.allFiles()
    missing = []
    for thisSheetName in allSheetNames:
        if thisSheetName not in allDirNames:
            missing.append(thisSheetName)
    return missing

def inDirNotInSheet():
    '''
    returns a list of files that seem to exist in the
    directory but are not in the spreadsheet.
    
    >>> import emmsap.fileAndSheet
    >>> import pprint
    >>> idnis = emmsap.fileAndSheet.inDirNotInSheet()
    >>> pprint.pprint(idnis)
    []
    >>> len(idnis)
    255
    '''
    wb = spreadsheet.Workbook()
    allSheetNames = wb.allFilenames()
    allAlternateNames = wb.allAlternateFilenames() 
    allDirNames = files.allFiles()

    missing = []
    for thisDirName in allDirNames:
        if thisDirName not in allSheetNames and thisDirName not in allAlternateNames and 'OMR_' not in thisDirName:
            missing.append(thisDirName)
    return missing
    


#-----------------------------------------
if __name__ == '__main__':
    music21.mainTest()