# -*- coding: utf-8 -*-
#----------------------------------
'''
Populates the MYSQL database using info from the directory and sheets

Run updateDB instead of this before searching via similarityDB
'''
import mysqlEM
# from emmsap import fileAndSheet
import files
# from emmsap import spreadsheet
try:
    from mysql.connector.errors import IntegrityError as IntegrityError # @UnresolvedImport
except ImportError:
    from pymysql import DatabaseError as IntegrityError

def populatePiecesSafe():
    '''
    safely populates the "pieces" table of the mysql directory by
    only finding pieces that aren't in it already
    '''
    em = mysqlEM.EMMSAPMysql()
    em.cursor.execute("SELECT id, filename FROM pieces")
    allfns = files.allFiles()
    for unused_pieceId, filename in em.cursor:
        if filename in allfns:
            allfns.pop(allfns.index(filename))
    print(allfns)
    query = '''INSERT INTO pieces (filename) VALUES (%s)'''
    for thisFn in allfns:
        try:
            em.cursor.execute(query, [thisFn,])
            pObj = em.pieceByFilename(thisFn)
            print(pObj.id, query, thisFn)
        except IntegrityError as e:
            print( str(e) )
    em.commit()


if __name__ == '__main__':
    populatePiecesSafe()
