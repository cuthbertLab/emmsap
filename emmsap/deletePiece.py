# -*- coding: utf-8 -*-

from emmsap import mysqlEM


def deleteOMRDuplicates():
    '''one time run to delete a bunch of duplicate OMR files'''
    pieces = [
        # delete second of each tuple
        (0, 92),
    ]
    em = mysqlEM.EMMSAPMysql()
    for unused_keep, deleteIt in pieces:
        p = mysqlEM.Piece(deleteIt, em)
        print(p.id, p.filename)

        p.deleteFileOnDisk()
        p.deletePiece()


if __name__ == '__main__':
    # deleteOMRDuplicates()
    # exit()
    # x = 3341
    for x in range(3345, 3368):
        emp = mysqlEM.Piece(x)
        print(emp.filename)
        emp.deletePiece(keepPieceEntry=False)
        emp.deleteFileOnDisk()
