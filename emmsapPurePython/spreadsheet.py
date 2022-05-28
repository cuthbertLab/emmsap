# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------

import music21
from music21 import common
from music21.ext import xlrd
from emmsap import files
import os

try:
    unicode # @UndefinedVariable
except NameError:
    unicode = str
    basestring = str

spreadsheetFp = os.path.join(files.emmsapBase,  'excelMetadata', 'transcription_pieces.xls')

class Workbook(object):
    '''
    represents the entire transcription spreadsheet
    '''
    def __init__(self):
        self.xbook = xlrd.open_workbook(spreadsheetFp)

    def sheetByName(self, sheetName):
        '''
        returns a Worksheet object given this name
        
        >>> import emmsap.spreadsheet
        >>> wb = emmsap.spreadsheet.Workbook()
        >>> wsCaccia = wb.sheetByName('caccia')
        >>> wsCaccia.totalRows
        33
        '''
        sheet = self.xbook.sheet_by_name(sheetName)
        return Worksheet(sheet)
    
    def allSheetNames(self):
        '''
        returns all sheetname in the book
        
        >>> import emmsap.spreadsheet
        >>> emmsap.spreadsheet.Workbook().allSheetNames()
        ['OVERVIEW', 'madrigal', 'caccia', 'ballata', 'liturgical', 'ballades', 'latin', 'virelais', 'rondeaux', 'laude', 'lost', 'non-Italian motets', 'misc', 'unidentifed']
        '''
        return self.xbook.sheet_names()
        
    def allSheetObjects(self):
        '''
        returns each sheet as a Worksheet object except the OVERVIEW object
        
        >>> import emmsap.spreadsheet
        >>> aso = emmsap.spreadsheet.Workbook().allSheetObjects()
        >>> aso[0:2]
        [<emmsap.spreadsheet.Worksheet "madrigal">, <emmsap.spreadsheet.Worksheet "caccia">]
        '''
        allSheetNames = self.allSheetNames()
        if allSheetNames[0].upper() == 'OVERVIEW':
            allSheetNames = allSheetNames[1:]
        allSheetObjs = [Worksheet(self.xbook.sheet_by_name(x)) for x in allSheetNames]
        return allSheetObjs
    
    def allFilenames(self):
        '''
        returns a list of all filenames in the spreadsheet

        >>> import emmsap.spreadsheet
        >>> afns = emmsap.spreadsheet.Workbook().allFilenames()
        >>> len(afns)
        1420
        >>> afns[0:2]
        ['PMFC_04_151-Si_dolce_non_sono.xml', 'PMFC_06_Giovanni-01-Angnel_son_biancho.xml']
        '''
        allFNs = []
        for thisWs in self.allSheetObjects():
            theseFns = thisWs.filenames()
            allFNs.extend(theseFns)
        return allFNs

    def allAlternateFilenames(self):
        '''
        returns a list of all alternateFilenames in the spreadsheet

        >>> import emmsap.spreadsheet
        >>> afns = emmsap.spreadsheet.Workbook().allAlternateFilenames()
        >>> len(afns)
        105
        >>> afns[0:2]
        ['PMFC_04_151-Si_dolce_non_sono.xml', 'PMFC_06_Jacopo_8-In_verde_prato.xml']
        '''
        allFNs = []
        for thisWs in self.allSheetObjects():
            theseFns = thisWs.alternateFilenames()
            allFNs.extend(theseFns)
        return allFNs
    
    def reportMisnamedFiles(self):
        '''
        Gives a list of all filenames that do not conform to POSIX (except length)
        standards.  Does not check alternate filenames.
        
        Returns a list of 4-tuples of the form (incorrect filename, fixed file name, row number, sheetname)
        
        >>> import emmsap.spreadsheet
        >>> from pprint import pprint as pp
        >>> ws = emmsap.spreadsheet.Workbook()
        >>> pp(ws.reportMisnamedFiles())
        []
        '''
        misnamed = []
        for ws in self.allSheetObjects():
            xmlFNcolumn = ws.indexByColumnName('xml filename')
            #print sn, xmlFNcolumn
            if xmlFNcolumn is None:
                continue
            for i in range(2, ws.sheetObj.nrows):
                rowValues = ws.sheetObj.row_values(i)
                if len(rowValues) < xmlFNcolumn:
                    #print len(rowValues), xmlFNcolumn, sn
                    continue
                xmlFN = rowValues[xmlFNcolumn]
                if xmlFN == '':
                    continue
                elif not isinstance(xmlFN, basestring):
                    continue
                fixedName = common.normalizeFilename(xmlFN)
                if unicode(fixedName) != xmlFN:
                    nameTuple = (xmlFN, fixedName, i, ws.sheetObj.name)
                    misnamed.append(nameTuple)
        return misnamed

        
class Worksheet(object):
    '''
    represents a single sheet in the transcription spreadsheet

    >>> import emmsap.spreadsheet
    >>> wb = emmsap.spreadsheet.Workbook()
    >>> ws = wb.sheetByName('caccia')
    >>> ws
    <emmsap.spreadsheet.Worksheet "caccia">
    >>> ws.headers[0:3]
    ['FischerNumber', 'Incipit', 'Voices']
    '''
    def __init__(self, sheetObj = None):
        self.sheetObj = sheetObj
        self.totalRows = sheetObj.nrows
        self.headers = sheetObj.row_values(1)
        self.lcHeaders = [unicode(x).lower() for x in self.headers]
    
    def __repr__(self):
        return '<emmsap.spreadsheet.Worksheet "%s">' % self.sheetObj.name
     
    def indexByColumnName(self, columnName = 'Incipit'):
        '''
        find the column index for the column of a given name
        
        Case insensitive matching.
        
        >>> import emmsap.spreadsheet
        >>> wb = emmsap.spreadsheet.Workbook()
        >>> ws = wb.sheetByName('caccia')
        >>> ws.indexByColumnName('PMFC')
        4
        >>> ws.indexByColumnName('BlahBlah') is None
        True
        '''
        cnLower = columnName.lower()
        try:
            return self.lcHeaders.index(cnLower)
        except ValueError:
            return None
        
    def filenameIndex(self):
        '''
        returns the index of the column number with 'xml filename'
        
        >>> import emmsap.spreadsheet
        >>> wb = emmsap.spreadsheet.Workbook()
        >>> ws = wb.sheetByName('caccia')
        >>> ws.filenameIndex()
        16
        '''
        return self.indexByColumnName('xml filename')

    def alternateFilenameIndex(self):
        '''
        returns the index of the column number with 'Alternate XML Filenames'
        
        >>> import emmsap.spreadsheet
        >>> wb = emmsap.spreadsheet.Workbook()
        >>> ws = wb.sheetByName('misc')
        >>> ws.alternateFilenameIndex()
        23
        '''
        return self.indexByColumnName('Alternate XML Filenames')


    def filenames(self):
        '''
        returns a list of all the non-null filenames in the sheet
        
        >>> import emmsap.spreadsheet
        >>> ws = emmsap.spreadsheet.Workbook().sheetByName('caccia')
        >>> fns = ws.filenames()
        >>> fns[0:2]
        ['PMFC_07_LdF_1_A_Poste_Messe.xml', 'PMFC_10_Zacherias_2-Cacciando_per_gustar_ai_cenci_ai_toppi.xml']
        '''
        nonNullFns = []
        fni = self.filenameIndex()
        if fni is None:
            return []
        for i in range(2, self.totalRows):
            cellVal = self.sheetObj.cell(i, fni).value
            if cellVal is not None and cellVal != '':
                nonNullFns.append(cellVal)
        return nonNullFns

    def alternateFilenames(self):
        '''
        returns a list of alternate filenames for the same pieces
        
        >>> import emmsap.spreadsheet
        >>> ws = emmsap.spreadsheet.Workbook().sheetByName('misc')
        >>> fns = ws.alternateFilenames()
        >>> import pprint
        >>> pprint.pprint(fns)
        ['PMFC_24A_1b-Con_lagreme_bagnandome.xml',
         'PMFC_24A_1c-Con_lagreme_bagnandome.xml',
         'PMFC_24A_1d-Con_lagreme_bagnandome.xml',
         'PMFC_24A_1e-Con_lagreme_bagnandome.xml',
         'PMFC_20_65a-Talent_m_a_pris.xml',...]
         '''
        nonNullFns = []
        fni = self.alternateFilenameIndex()
        if fni is None:
            return []
        for i in range(2, self.totalRows):
            cellVal = self.sheetObj.cell(i, fni).value
            if cellVal is not None and cellVal != '':
                altFns = cellVal.split(';')
                for altFn in altFns:
                    altFn = altFn.strip()
                    nonNullFns.append(altFn)
        return nonNullFns



#------------------------------
if __name__ == '__main__':
    music21.mainTest()
    
