from emmsap import mysqlEM

def deleteOMRDuplicates():
    '''one time run to delete a bunch of duplicate OMR files'''
    pieces = [              # delete second
               (0, 92), # 
    ]
    em = mysqlEM.EMMSAPMysql()
    for unused_keep, deleteIt in pieces:
        p = mysqlEM.Piece(deleteIt, em)
        print(p.id, p.filename)
        
        p.deleteFileOnDisk()
        p.deletePiece()


if __name__ == '__main__':
    deleteOMRDuplicates()
    exit()
    p = mysqlEM.Piece(608)
    print(p.filename)
    p.deletePiece()
