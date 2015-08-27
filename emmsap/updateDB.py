from emmsap import indexFiles
from emmsap import indexSegments
from emmsap import indexRatios
from emmsap import indexTexts
from emmsap import indexTinyNotation

def updateDatabase():
    '''
    adds any files in the EMMSAP musicxml_in dir to the database.
    '''
    indexFiles.populatePiecesSafe()
    indexSegments.updateSegmentTable('DiaRhy2')
    indexRatios.updateRatioTable('DiaRhy2')
    indexTexts.runAll()
    indexTinyNotation.runAll()

if __name__ == '__main__':
    updateDatabase()