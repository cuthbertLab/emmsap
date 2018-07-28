from emmsap import indexFiles
from emmsap import indexSegments
from emmsap import indexRatios
from emmsap import indexTexts
from emmsap import indexTinyNotation


def updateDatabase():
    '''
    adds any files in the EMMSAP xmlData dir to the database. 
    '''
    indexFiles.populatePiecesSafe()
    indexSegments.updateSegmentTable('DiaRhy2')
    indexRatios.updateRatioTableParallel('DiaRhy2')
    indexSegments.updateSegmentTable('IntRhySmall')
    indexRatios.updateRatioTableParallel('IntRhySmall')
    indexTexts.runAll()
    indexTinyNotation.runAll() # also does intervals
    print('Done!')

# every once in a while run: 
# DELETE FROM ratiosDiaRhy2 WHERE segment1id NOT IN (SELECT id FROM segment)
# takes about a minute, but speeds up everything!

if __name__ == '__main__':
    updateDatabase()
