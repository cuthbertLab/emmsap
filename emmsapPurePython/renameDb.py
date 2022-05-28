'''
rename one or more files in the database taking into account all places
that use the filename as an identifier
'''
from emmsap.mysqlEM import EMMSAPMysql

em = EMMSAPMysql()

def renameTable(tableName, fnColumn, old, new):
    query = 'UPDATE {tableName} SET {fnColumn} = %s WHERE {fnColumn} = %s'.format(
                                                            tableName=tableName,
                                                            fnColumn=fnColumn)
    em.cursor.execute(query, (new, old))

def renameOnePiece(old, new):
    renameTable('intervals', 'fn', old, new)
    renameTable('pieces', 'filename', old, new)
    renameTable('texts', 'fn', old, new)
    renameTable('tinyNotation', 'fn', old, new)

def getFixNames(vol='16'):
    em.cursor.execute(
        'SELECT filename FROM pieces WHERE filename REGEXP "^PMFC' + vol + '"')
    return([(x[0], x[0].replace('PMFC', 'PMFC_')) for x in em.cursor])
    

def main():
    for old, new in getFixNames('16'):
        renameOnePiece(old, new)

if __name__ == '__main__':
    #renameOnePiece('Arras_941_ballade_c.xml', 'Arras_941_Ballade_C.xml')
    main()
    