import os
import sys
import json
import collections
import codecs
import datetime
import music21
import re

parentPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", '..', '..'))
#sys.stderr.write('UGGG: ' + parentPath + ' \n')
sys.path.append(parentPath)

import emmsap
import emmsap.mysqlEM
from emmsap import toTinyNotation

class Main(object):
    def __init__(self, f = None):
        self.em = emmsap.mysqlEM.EMMSAPMysql()
        self.form = f
        self.jsonForm = None
        self.useJsonP = False
        self.parseForm()
        
    def parseForm(self):
        if self.form is None:
            return
        if 'json' not in self.form:
            return
        jsonString = self.form.getfirst('json')
        self.jsonForm = json.loads(jsonString)
        if 'jsonp' in self.form:
            self.useJsonP = True
            self.jsonPCallFunction = self.form.getfirst('jsonp')        
        elif 'callback' in self.form:
            self.useJsonP = True
            self.jsonPCallFunction = self.form.getfirst('callback') 
            
        return self.jsonForm

    def err(self, msg=""):
        msg = str(msg)
        sys.stderr.write("AtlasBackend: " + msg + "\n");
    def printJsonHeader(self):
        if self.useJsonP:
            ct = 'application/javascript'
        else:
            ct = 'text/json'
        print("Content-Type: " + ct)
        print("")
                
    def jsonReply(self, pyObj):
        self.printJsonHeader()
        jsonString = json.dumps(pyObj)
        if self.useJsonP is not True:
            print(jsonString)
        else:
            print(self.jsonPCallFunction + "(" + jsonString + ")\n")

    def searchTN(self):
        self.err(self.form)
        if 'query' not in self.jsonForm:
            return
        tnPre = self.jsonForm['query']
        if 'octaveEquivalent' in self.jsonForm:
            octaveEquivalent = self.jsonForm['octaveEquivalent']
        else:
            octaveEquivalent = False
        
        if 'modalTransposition' in self.jsonForm:
            modalTransposition = self.jsonForm['modalTransposition']
        else:
            modalTransposition = False
            
        if octaveEquivalent is True or modalTransposition is True:
            binarySearch = ''
        else:
            binarySearch = 'BINARY'
        self.err(binarySearch)
        
        s = music21.converter.parse('tinyNotation: ' + tnPre)
        
        if modalTransposition is not True:
            outRows = self.getMatchingRows(s, binarySearch)                    
        else:
            outRows = []
            for genericInterval in range(1, 8):
                sTransposed = s.transpose(music21.interval.GenericInterval(genericInterval))
                newRows = self.getMatchingRows(sTransposed, binarySearch)
                outRows = outRows + newRows
        
        self.jsonReply(outRows)
    
    def getMatchingRows(self, s, binarySearch):
        outRows = []
        excerptNumNotes = len(s.flat.notes)
        tn = toTinyNotation.convert(s.flat.notesAndRests) # regularize
        # BINARY below forces case sensistive...
        self.em.cursor.execute('SELECT fn, partId, tsRatio, tn FROM tinyNotation WHERE tn LIKE ' + binarySearch + ' "%' + tn + '%"')
        rows = self.em.cursor.fetchall()
        for r in rows:
            j = {}
            j['fn'] = r[0]
            j['partId'] = r[1]
            j['tsRatio'] = r[2]
            allTn = r[3]
            excerptIndex = allTn.lower().find(tn.lower())
            if (excerptIndex == -1):
                continue # case sensitivity or something...
            contextStart = excerptIndex - 12
            contextEnd = excerptIndex + len(tn) + 12
            if contextStart < 0:
                contextStart = 0
            if contextEnd > len(allTn):
                contextEnd = len(allTn) - 1
            context = allTn[contextStart:contextEnd]
            context = context.strip()
            context = re.sub('^\S+\s+', '', context)
            context = re.sub('\s+\S+$', '', context)
            excerptMatchStart = context.lower().find(tn.lower())
            excerptNoteStart = context.count(' ', 0, excerptMatchStart)
            j['excerptNoteStart'] = excerptNoteStart
            j['excerptNoteEnd'] = excerptNoteStart + excerptNumNotes
            j['context'] = context
            outRows.append(j)
        
        return outRows