'''
Separating out a large pdf for OCR is hard -- this will help move
files into the right place for Sharp score
'''
import os
import shutil

inDir = '/Users/Cuthbert/desktop/CMM_Dufay_In/'
inPreface = 'Dufay_6_Page_'
outDir = '/Users/Cuthbert/desktop/CMM_Dufay_Out/'
outPreface = 'Dufay_6_'


def mkDirs(maximum=100):
    for i in range(1, maximum):
        iStr = "%02d" % i # change as needed
        os.mkdir(outDir + iStr)


class Mover:
    def __init__(self):
        self.lastPageNum = 11
        self.lastFileNum = 0

        self.skip_on_file_not_found = False
        self.usePreEdited = False

    def moveNList(self, nList, *, startNum=1):
        self.lastPageNum = nList[0] - 1
        self.lastFileNum = startNum - 1
        for i in range(1, len(nList)):
            startPageOf_Next_Piece = nList[i]
            endPageOf_This_Piece = startPageOf_Next_Piece - 1
            self.moveToN(endPageOf_This_Piece)

    def moveToN(self, n):
        '''
        move some tif files from lastPageNum + 1 to n
        to lastFileNum + 1; and increment
        '''
        startPageNum = int(self.lastPageNum + 1)
        thisFileNum = self.lastFileNum + 1
        if not self.usePreEdited:
            moveRangeAdjust = 1 if isinstance(n, int) else 2  # float means to keep two copies...
        else:
            moveRangeAdjust = 1

        for pn in range(startPageNum, int(n) + moveRangeAdjust):
            pnIn = inDir + inPreface + "%03d.tiff" % pn
            pnOut = outDir + "%02d/%s%02d_%03d.tif" % (thisFileNum, outPreface, thisFileNum, pn)
            print(pnIn, pnOut)
            try:
                shutil.copy2(pnIn, pnOut)
            except FileNotFoundError as fnf:
                if not self.skip_on_file_not_found:
                    raise fnf
                else:
                    pass

        self.lastPageNum = n
        self.lastFileNum = thisFileNum


if __name__ == "__main__":
    # mkDirs()
    m = Mover()
    # m.moveToN(18)

    # PMFC 14
    # m.moveNList([13, 15, 16, 17, 20, 22, 23, 25, 26, 28, 28, 29, 30,
    #              32, 34, 36, 37, 38, 39, 41, 42, 43, 45, 46, 48, 51,
    #              56, 58, 61, 62, 65, 67, 71, 73, 76, 78, 81, 83, 85,
    #              87, 90, 93, 95, 96, 99, 101, 102, 104, 107, 109, 110, 112,
    #              114, 116, 119, 121, 123, 125, 128, 130, 133, 137, 138, 140, 141,
    #              146, 147, 149, 151, 154, 158, 160, 163, 164, 167, 170, 172, 173,
    #              175, 176, 177, 179, 182, 183, 184, 185, 187, 188, 190], startNum=1)
    # PMFC 14 appendix
    # m.moveNList([190, 191, 192,
    #              195, 199, 200, 202, 203, 204, 206, 209, 211, 213, 215, 217, 220,
    #              224, 225, 227, 228, 230, 233, 234, 237, 239, 241, 243, 247], startNum=1)

    # PMFC 15
    # m.moveNList([12, 19, 24, 27, 30, 33, 36,
    #              40, 43, 47, 51, 57, 64, 70,
    #              75, 79, 83, 88, 93, 96, 101,
    #              104, 111, 117, 122, 125, 129,
    #              131, 133, 137, 140, 144, 147,
    #              153, 158, 164, 167], startNum=1)
    # PMFC 17
    # m.moveNList([8, 12, 14, 15, 16, 17, 18, 19, 20, 21,
    #              25, 26, 28, 31, 35, 41, 42, 44, 48, 50,
    #              53, 54, 55, 58, 59, 61, 63, 64, 66, 68,
    #              71, 72, 74, 77, 80, 82, 84, 89, 94, 95,
    #              97, 98, 99, 102, 105, 107, 110, 115, 119, 124,
    #              129, 135, 138, 140, 142, 145, 149, 156, 157, 160,
    #              163, 165, 167, 170, 171, 175, 176, 178, 179
    #              ], startNum=1)

    # PMFC 15 SUP (in PMFC 17) # #4 rename to #5
    # m.moveNList([231, 235, 238, 241, 244], startNum=1)

    # PMFC 02 lays
    # m.moveNList([5, 6, 9, 14, 19, 23, 26,
    #              30, 34, 38, 43, 56, 79,
    #              85, 89, 94, 98, 103, 106,
    #              110, 111, 112
    #              ])
    # E15cM 3
    # m.moveNList([39, 39, 40, 41, 42,
    #              43, 46, 49, 52, 56,
    #              59, 62, 63, 64, 66,
    #              69, 72, 78, 80, 82,
    #              84, 87, 91, 93, 95,
    #              96, 97, 100, 101, 102,
    #              104, 107, 110, 113, 116,
    #              118, 119, 124, 126, 130,
    #              131, 133, 135, 136, 140,
    #              141, 142, 144, 146
    #              ])

    # Turin vol. 4
    # m.moveNList([1, 2., 3., 5, 6, 8, 9., 11., 12., 14,
    #             15, 16., 18, 19., 20., 21., 22., 23., 25., 27,
    #             27., 29, 30., 31., 33, 34, 34., 36, 37, 38.,
    #             39, 39., 40., 41., 42., 43, 44, 45., 46., 47.,
    #             48, 49., 50., 52, 53, 54., 55., 56., 58, 60.,
    #             61, 62., 63., 64., 65., 67., 68., 69., 70., 71.,
    #             73, 74., 75., 76., 78
    #              ])

    # # CMM 79 part 1
    # # m.usePreEdited = True
    # m.moveNList([38, 39, 40, 43, 45., 47, 49, 55, 57, 59, 60, 61, 63,
    #              65, 66, 67, 69, 70., 72, 73., 75, 77, 79, 80, 81, 84.,
    #              86, 87., 89, 90, 92, 93, 94, 99, 99., '99c'])

    # Dufay Volume 6
    m.skip_on_file_not_found = True
    m.moveNList([83, 84, 86., 88, 89, 92, 93, 94,
                 97, 101, 107, 109, 110., 111, 112, 113, 115, 116.,
                 118, 119, 121, 123, 124., 125., 127, 131, 132, 133, 133., 134.,
                 135., 136., 136., 137., 138., 139, 139.,
                 140., 141, 142, 142., 143., 144, 145, 146., 147, 148, 149, 150,
                 151., 152., 153., 154, 154., 156., 157, 157., 168., 159, 160,
                 161, 162, 163, 164, 164., 165., 166, 166.,
                 167., 168, 169, 170, 170., 171., 172., 173, 174, 174., 175.,
                 176., 177., 178, 178., 179., 183, 184., 187, 188, 189.,
                 190, 191, 192, 193, 193.
                 ])
