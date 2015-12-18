# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from __future__ import print_function
from emmsap import mysqlEM
#from music21.search import segment


skipPieces = [             
               # new discoveries!
               (338, 2087), # Ciconia Credo 11 = Prague 9 O sinne!!!
               (2107, 2080), # Prague_9_35_Scheiden_wie and Je en vos (Jeo_hay) ed. Fallows
               
               (1964, 1227, 1229, 334), 
                   # Machaut Motet 4 Puis que la douce + PMFC5.17 Fortune Mere a Dolor 
                   # (+ not found b/c transposed Amer amours/Durement PMFC 5.19 ) / 
                   # close similarity to PMFC 23.64 Patrem ab eterno tenor, but not close enough
               (1961, 1097), # Quant en moy/Amour et biaute (Machaut M1) m80 +
                   # Colla/Bona Condit (Vitry?) m1 (and many other matches)
               (28, 1845), # Esperance +  Santa maria maggiore fragments
               (1596, 481, 482), # Onques ne fu ; Vendome contratenor.
               (285, 1959), # Nuremberg9a gloria fermatas: Gloria Clementiae Pax
               (808, 1899), # Houghton 122 Patrem and Salinis Patrem                              
               (1585, 664), # Fist on dame -- Paris Lat 12409 -- too short so ratio is only 7352, 
                    # but found in tinynotation search
               (1999, 325), # Feragut Patrem #2 and Credo Tapissier -- same tenors, 
                    # same # of breves but only at Deum vero + Genitum
               
               
               (2064, 1912), # Nicolaus de Radom Gloria 1 + Credo 1 paired; see esp. Adoramus te
                            # + Genitum non Factum.
               # end new discoveries.
               
               # two transcriptions of the same
               # same piece..different versions.
               (2194, 2195), # FallowsMB_89 + 89a
               (2167, 2168), # So ye emp. Fallows 64 + 64a
               (2198, 2199), # FallowsMB_092_N_aray_je_jamais.mxl
               (2169, 2170, 2171), # 15th c. O Rosa Bella Complex
               (2164, 2165, 747), # FallowsMB_062_Gentil_madonna.mxl 
                        # FallowsMB_062a_Fortune_alas.mxl, Boverio nachtrag version
               (2161, 2162), # FallowsMB_060_Mon_seul_plaisir.mxl FallowsMB_060a_Mi_verry.mxl
              (1774, 1775), # two versions Sedendo al onbra
              (1771, 1772), # two versions Piu non mi curo
              (1767, 1768), # two versions O tu chara scientia
              (1904, 1378), # E15cM + Stoessel version Salinis En la saison
              (1296, 1408), # PMFC and Stoessel version Zachara Sol mi traffig
              (650, 651), # merce o morte two versions PMFC 20
              (22, 257, 536, 820), # Philippcoctus Credos
              (34, 184), # donna si to fallito
              (33, 683), # de non fugir
              (35, 673), # fortuna ria
              (1454, 38), # si te so stato
              (1455, 669, 84),
              (252, 251, 819, 784, 785), # PMFC 12 10a/10b, PMFC 13 A7, PMFC 13.26, 27
              (253, 254), # PMFC 12 11a/11b 
              (1464, 690),
              (1463, 688),
              (798, 1412), # Puer natus
              (1462, 684),
              (710, 1347), # plorans
              (711, 1405), # du val pilleus
              (712, 1377), # Par les bons Gedon
              (740, 1438), # Si fort
              (738, 1437), # Se ie ne suy
              (861, 1439), # Jaym la plus belle
              (1567, 766), # Paolo Sofrir printed in 9 and 21.
              (1504, 1503), #PMFC 9.26a/b
              (65, 1351), # Marot
              (73, 1343), # Alta regina
              
              (1530, 1531), 
              (1536, 1537),
              (1541, 1542, 638, 639), #ep 1541 later
              (1544, 1545, 1925),  # Je voy mon cuer, Du asserweltes schons
              (1550, 514), # 514 low match OMR gloria
              (1553, 1554),  # Mersi ou mort -- two versions
              
              
              (1478, 1479),
              (48, 62),   # Jacopo O cieco mondo
              (449, 1415), # two versions En attendant
              (461, 1427), # two versions en remirant
              

              (862, 863, 864, 1440),
              (1452, 260),
              (1464, 690, 1141),
              
              (41, 576, 1195), # Gdansk, Gloria, Ghent # found before EMMSAP
              (827, 568), # 23.40
              (828, 569), # 23.41
              (365, 366), # Ciconia: two versions of merce o morte 
              
              (1576, 1956), # two very different versions of Dame_par_vous_douch_plaizir

              (381, 382, 383, 384, 385), # keyboard con lagrime versions
              (346, 372), # Ciconia, aler, o beatum
              (358, 359), # Ciconia: ligiadra donna two versions
              (509, 510), # celice agentem : found w/o EMMSAP by MSC
              (63, 549, 809), # oxford sanctus -- mine (63) is better
              (226, 227), # bartolino alba cholumba
              (224, 225), # bartiolino non correr
              (850, 718, 727, 1252, 718), # three versions Credo Deus Deorum + Song
              (862, 863), # two versions conbien que lontain
              
              (857, 261), # pmfc 23.69 Sanctus = Mediolano
              (853, 722), # pmfc 13.23 Zachara -- Boverio version
              (721, 749, 851), # pmfc 13.21 Zachara -- Boverio versions
              (855, 331), # Sanctus PMFC 23.67, PMFC 23.61 Credo -- False match
              (322, 582), # Gloria Peliso -- 322 by hand, incomplete; 582 smartscore
              (396, 588), # sant omer -- me, depricate 588 pmfc
              (746, 443, 1441), # 3 version Pictagoras Jubol
              (715, 1442), # Virtute_sacquista_cum_grande_faticha
              (1997, 76), # two versions B Feragut De yre et de Dueyl
              
              (1405, 711), # du val pilleus
              (744, 745), # two version Tu me solevi donna
              (725, 368), # non credo donna -- PMFC + Marchi versions
              (304, 489, 719, 723), # Damor languire, Credo Scabioso (PMFC, Marchi, MSC Completion)
              (791, 287, 1061), # questa fanciulla Kyrie and Agnus Dei, original
              (305, 306), # humano genere      
              (286, 313), # kyrie summe clementissime
              (115, 477, 937), # Je porte Donatus
              (15, 420), # Se Zephryus -- Budapest and Stoessel version
              (276, 30), # gaudeamus
              (86, 671), # why so lo on same piece?
              (877, 796), # Iste Confessor: PMFC 23_83a and PMFC 13_39 (83b is not related)
              (880, 839), # PMFC 23_35 / 36 ??
              (1098, 201), # Jacopo with Faenza
              (1124, 971), # Jacopo with Faenzo
              (1080, 1196), # Credo de rege, 1196 is additional version
              (1177, 396), # PMFC Sant Omer Sanctus, MSC version = 396.
              (1164, 406), # Madrid CT/T, Siena Ravi 3 3vv version -- found Nyikos, pre PMFC
              (1260, 969), # Inter_Denasas_Deserti_Meditans
              (1598, 1599, 172, 174), # two versions of Or sus + a keyboard piece
              (1589, 1590, 21), # two versions Je voy le bon tens + false match 
                #    with gloria in Cividale
              (1888, 1889), # Tres douls amis, two versions
              (1886, 1241), # Souviengne vous d estriner, Quand amor -- Fetis, identical
              
              (1923, 1924), # two Wolkenstein versions of Des himels trone
              (1943, 1944, 1449), # two versions Wolkenstein Wol auf wol an and low
                # match for Levandome l maytino
              (1931, 1932), # two versions Herz mut leib sel, Wolkenstein
              
              
              
              
              ######
              # known similarities
              (2125, 888), # FallowsMB_028_Min_herze_wil and PMFC 23.91 O_Quam_Pulchra_Puella ctrft
              (2093, 291), # Zachara, Fior Gentil and Gloria
              (2050, 2018), # Machaut motets 21 and 8 -- Earp p. 367
              (1977, 1678), # Ma dame m'a congie doune quotes from Machaut B15 
                # Se je me pleing (Low match: only 6875 but completely there!)
              (1558, 1720), # S'espoir n estoit + Machaut Se vous n'estes -- in Earp book
              (1687, 1525, 602), # Machaut De fortune, Dame qui fust -- known;
                # De fortune well known in Italy! Dame qui fust, Reina only
              (290, 1288), # rosetta + gloria
              (1601, 889, 2123), # pmfc 21.5 contrafacted as 23.92, included also in Fallows
              (320, 1216), # Gloria Loys, Flos Ortus Inter Lilia (Known)
              
              (32, 266, 270, 271, 272, 389, 390, 398, 480),  # flos filius benes
              (299, 300), # Gloria PMFC 13 14-15 -- same tenor
              (220, 229), # bartolino amor che nel pensier, l invido per lo ben
              (172, 174, 175), # Faenza Kyrie, Gloria, Ave Maris Stella
              (971, 170, 386, 152, 172, 32), # Faenza Jacopo da Bologna 
              (168, 171, 397, 388), # kyries based on Cunctipotens
              (167, 31), # verbum caro...
              
              (373, 461, 1427), # ciconia Sus un Fontayne, En remirants
              (351, 352), # per quella strada 74-80, una pantera 13-15
              (215, 351), # imperial sedendo, per quella strada
              
              (856, 868, 1184), # Sanctus Sanans Fragilia PMFC 23.68 w/ Agnus Dei PMFC 23 74
                # PMFC 23.4 (Sorbonne Sanctus),
              (1150, 1184, 1185, 1156), # Sorbonne Mass internal consistencies 
                # and w/ Kyrie Sol Iusticie
              (1180, 1171, 1161), # PMFC 23 13, PMFC 23.12, PMFC 23.11 -- known;
              (1092, 908), # Tournai Ite Missa, Ave Regina Mater Innocencie 
                # also on same Ite Missa tenor
              (1227, 1229), # PMFC 05 # 17 and 19 -- same tenor.
              
              
              
              
              
              # unknown similarities worth mentioning...
              (2025, 1961), # Machaut Motet 15 (m. 59-102) and Machaut Motet 1 (m. 122-end) 
                # same melodic formula
              (373, 993), # Ciconia & Francesco!  Sus une fontayne and Che pena quest al cor -- 
                # very similar cadential strategies.
              (140, 144), # Lorenzo -- Credo che i donna (T 125, 131), Come in sul Fonte 
                # from (63, 69) -- D to G descent
              (204, 207), # Giovanni Appress un fium 33, Donna gia fu 16
              (104, 106), # Donatus -- Un cane un oca 76-77; Sovran ucell 23-24
              (119, 211), # GdF Si Forte 41-47; Piero All onbra 46-52
              
              (1573, 1142), # PMFC 21.22, 10.23 -- similar cadences, but not a quote.
              (1495, 259),  # Nicolo Virtu loco non + Sanctus PMFC 12.16 -- anon RVat 1419 -- 
                # not a quote but may be an attribution.
              
              (1481, 1236), # Nicolo and Bonaiuto
              (1494, 1487, 1463), # two Nicolo w/ similar ornamentation. + a francesco w/ similar
              
              
              
              
              
              
              
              
              # low threshold false matches
              (1963, 388, 807, 169, 1488), # Machaut M3 and Ravenna Kyrie, + instrumental Faenza  
                # + Nicolo melisma
              (1962, 1474), # machaut M2 + PMFC 8-34 Pyance. No.
              (1967, 1236, 1641, 32, 815, 755, 1641), # Empris domoyres w/ much noodling.
              (1965, 370, 687, 1641, 386), # Machaut M6
              (687, 981), # 04_35-Il_suo_bel_viso, PMFC_04_111-Amore_in_te_spera (7000)
              (1961, 1306, 1095, 397), # Machaut Tenor M1 Amour et biaute + Nicolo de come
                # ben mi sta, Garison selon Nature, Barcelona Kyrie
              (99, 1338, 1303), # DfF L aspido Sordo + Una smaniosa PMFC 8
              (119, 1170), # madrigal patterns
              (140, 1768), # madrigal patterns
              (168, 1767), # madrigal patterns + keyboard
              (172, 1306), # madrigal patterns + keyboard
              (107, 1802), # Come da lupo, Graciosa Petra
              (1853, 1252), # Arras 941 si vous plait, Deus deorum pluto
              (1905, 1451), # Arras 941 Patrem, nel prato pien di fiori
              (1509, 260),
              (1493, 202),
              (2182, 401), # Addio...
              (1509, 602),
              (1567, 761), # two paolo pieces...
              (1655, 187), # 22.47b, 04.04.
              (1118, 939), # PMFC 06 Jacopo Vestisse, PMFC 07 GdF 2 -- Cacciand -- filigree
              (1141, 37), # PMFC 10 22 Perche veder non posso; Francesco Poy che Partir -- 
                           # very similar cadence
              (1183, 465), # Credo Sorbonne, Lorques Arthus -- filigree
              (211, 149), # Piero All ombra, VdR Gia Era
              (255, 386), # bartholus Credo w/ Deduto Sey intabulation
              (863, 862, 187), 
              (3, 860),
              (860, 118),
              (860, 68),
              (858, 146),
              (858, 351),
              (351, 2009), # low match, Per quella Strada. PMFC 16-03 Agnus Dei
              (141, 665),
              (807, 1314),
              (101, 769),
              (1227, 1306),
              (1229, 1306),
              (124, 209),
              (215, 769),
              (99, 144),
              (1280, 809),
              (37, 690),
              (815, 919),
              (769, 351),
              (857, 276),
              (331, 320), # Gloria Loys, Credo 23.61 -- some tenor similarities but not enough
              (32, 240), # intab w/ melisma
              (148, 465),
              (138, 352), # una pantera with lorenzo.
              (48, 350), # o cieco mondo
              (104, 270),
              (48, 350), # jacopo + ciconia i cani # some similarities -- 
              (174, 386),
              (188, 354),
              (104, 270),
              (1869, 330),
              (1869, 1095), 
              (1879, 306),
              (691, 1040), # PMFC_04_39-Nella_partita PMFC_04_76_Abbonda_di_virtu (7000)
              
              (1579, 974), # E dieus commant + Giunta vaga bilta
              (1677, 1481), # Machaut Je ne cuit + Nicolo Non si conosce

            # IGNORE Tenors only...
            (2094, 166), # Autun 152 Deo Gratias + PMFC 12_44 Ave Verum Corpus -- not close enough
            (1982, 1163), # Turin 2b Patrem, PMFC 23.112 Gloria
            (1964, 32), # flos filius matches everything...
            (1080, 1097), # Barcelona Credo, Vitry Bona Condit
            (1083, 276), # Toulouse Kyrie, Gaudeamus Omnes
            (1084, 865), # Toulouse Sanctus, Credo Pellisson
            (1088, 480), # Tournai Gloria, Benedicamus Domino
 
            (1911, 1217, 331, 334), # Per grama tenor... w/ some credos.
            (397, 1227, 1229),
            (388, 1314), # Ravenna Kyrie + PMFC_08_Nicolo_18-It_a_veder_ciascun.xml
            (388, 1770), # Ravenna Kyrie + Per ridd andando
            (386, 739, 769), # keyboard deduto sey.
            (386, 1772), # keyboard deduto + Piu non mi churo
            (1445, 1184, 306),
            (1097, 328), # PMFC 1, 9 Bona Condit and Credo 23.57
            (1096, 1095), # Hugo Hugo, Garison
            (1095, 907), # Hugo Hugo, Dulcis Jesu
            (32, 159), # Flos Filius tenor, Marchetto Ave Regina
            
            (170, 172, 175, 169, 173, 386, 170, 383, 382, 386, 32, 258, 152, 100, 919), 
                # intabulations...and matches
            
            (903, 406), # Ortorum Virentium, Gloria Ravi 3 tenors not close
            (276, 334, 330, 331), # close range tenors not close
            (907, 904), # close range tenors not close
            (27, 334), # T
            (29, 270), # T
            (970, 151), # porta celi and In Forma Quasi
            (330, 303, 328),
            (276, 155), 
            (397, 276), # T Gaudeamus omnes, Kyrie
            (179, 155), # no.
            (169, 168), # rhythmicized intab tenor -- close rhythm but not match
            (149, 485),
            (159, 271),
            (320, 334), 
            (1530, 349),

            (2012, 398), # PMFC 16.06 Kyrie Kyria Christifera w/ Seville 25 B.D. frag (nope)
        
            (140, 215, 1772), # PMFC_07_LdF_2_Come_in_Sul_Fonte; 
                # PMFC_09_Bartolino_10-Inperial_sedendo PMFC_06_16b-Piu_non_mi_churo
            (165, 270), 
            (485, 149), 
            (374, 147), # quod jactatur
            (114, 306), # kyrie + madrigal
            (866, 276), # Credo 23.58 w/ Gaudeamus Omnes -- no.
            (892, 270),
            (891, 172, 179, 352),
            (897, 170, 807),
            (27, 30), # in medio, gaudeamus 
            (240, 907),
            (904, 907), 
            (248, 397),
            (276, 351, 306),
            (174, 386),
            (320, 328),
            (1077, 326),
            (27, 276, 904, 179), # Dubrovnik In Medio, Gaudeamus Omnes, Ave Jesu Christe
            (971, 169),
            (331, 1216),
            (320, 1230),
            (306, 936),
            (338, 1227),
            (338, 1229),
            (207, 927),
            (165, 1320),
            (149, 1314),
            (141, 196),
            (397, 1227),
            (99, 1338),
            (260, 1357),
            (276, 1264), # Gaudeamus_Omnes + Musicalis_Sciencia 
            (276, 1337), # Gaudeamus_Omnes +  PMFC_08_Nicolo_24
            (276, 1357), # Gaudeamus_Omnes + PMFC_10_Caserta_7-Piu_chiar_che_l_sol
            (1494, 688), # renamed...
            (1469, 1270),
            (2119, 326), #FallowsMB_021_Mon_cuer.mxl Credo_Tailhandier.mxl nope.
            (2122, 398), # FallowsMB_024_Felix_namque.mxl Seville_25_Benedicamus_Domino nope.
            (63, 1280),
            (1451, 1277),
            (149, 1314),
            (171, 1306),
            (179, 1228),
            (178, 1213),
            (1451, 932),
            (1451, 63, 809),
            (1458, 807),
            (1467, 351, 1107),
            (1466, 1303),
            (1464, 37),
            (1473, 100),
            (1467, 209, 1083),
            (1483, 1321),
            (1486, 1280),
            (1487, 1466, 1473, 1338),
            (1487, 927, 939, 209),
            (1487, 107, 1243),
            (1487, 935, 1034),
            (1488, 696),
            (1030, 172, 1277), # PMFC_12_A5-Kyrie_PMFC12_A5
            (904, 30),
            (919, 174),
            (908, 32),
            (1488, 30, 276), # tenor. no
            (903, 1263),
            (1489, 1072),
            (1655, 1656, 1657), # pmfc 22.47 many versions
            (1655, 1408),
            (306, 1271),
            (305, 306, 7272), # Kyrie + PMFC 11.32
            (27, 1230),
            (1641, 1488, 330, 215, 32, 1451, 168, 386, 172, 328), #keyboard
            
            (1983, 1984), # Turin masses OMR w/ cropped sections redone.
            (1995, 1829), # Turin mass tenor low match with PMFC 22.46
            (2008, 1096), # PMFC16 sanctus 2; low w/ Vitry Hugo Tenor
            (2009, 1965), # PMFC16 #3 Agnus; PMFC 2 SAmours tous amas joir. 
            (2015, 100), # kyrie PMFC 16 9 + melisma
            
            (2022, 1280), # machaut tenor + melismatic piece
            (2025, 1961), # two machaut tenors
            (2136, 1267), # FallowsMB_039_Quene_note.mxl PMFC8 Du_ancoliti
              ] 

class SimilaritySearcher(object):
    def __init__(self, startPiece=20, endPiece=2500, minThreshold=7500, maxToShow=1):
        self.dbObj = mysqlEM.EMMSAPMysql()
        self.startPiece = startPiece
        self.endPiece = endPiece
        self.minThreshold = minThreshold
        self.maxThreshold = 10001
        self.segmentType = 'DiaRhy2'
        self.skipGroups = skipPieces
        self.maxToShow = maxToShow
        self.tenorThresholdAdd = 500
        self.tenorPartNumber = 2
        self.tenorOtherPartNumber = 2
        self.printOutput = True
        
    def runPieces(self, startPiece=None, endPiece=None):
        '''
        The main algorithm to search for pieces to match
        
        minThreshold, maxThreshold, and tenorThresholdAdd are numbers from 0 to 10,000+ which scale
        to 0 - 1 (by dividing by 10000) to find similarity.
        
        Because of their rhythmic similarity, tenors match far too often, so a crude metric is used
        to identify tenors and raise the minThreshold for those matches: basically, 
        parts 2+ (=3rd part
        and beyond) are considered tenors. Not very good, but the best so far. 
        '''    
        if startPiece is None:
            startPiece = self.startPiece
        if endPiece is None:
            endPiece = self.endPiece
        
        for pNum in range(startPiece, endPiece):
            self.runOnePiece(pNum)

    def runOnePiece(self, pNum):
        skippedPieces = []
        p = mysqlEM.Piece(pNum, dbObj=self.dbObj)
        if p.id is None:
            return
        print("Running piece %d (%s)" % (pNum, p.filename))
        ratioMatches = p.ratiosAboveThreshold(self.minThreshold, 
                                              ignoreInternal=True, 
                                              segmentType=self.segmentType)
        totalShown = 0
        for ratioMatch in ratioMatches:
            returnCode = self.checkOneMatch(p, ratioMatch, totalShown, skippedPieces)
            if returnCode is not None:
                totalShown = returnCode

    def ratiosForPiece(self, pNum):
        p = mysqlEM.Piece(pNum, dbObj=self.dbObj)
        if p.id is None:
            return
        ratioMatches = p.ratiosAboveThreshold(self.minThreshold, 
                                              ignoreInternal=True, 
                                              segmentType=self.segmentType)
        return ratioMatches

    def checkForShow(self, p, ratioMatch, skippedPieces=None):
        if skippedPieces is None:
            skippedPieces = []
        myId = p.id
        if ratioMatch.thisRatio >= self.maxThreshold:
            return (False, "MaxThreshold")
        otherSegment = mysqlEM.Segment(ratioMatch.otherSegmentId, dbObj=self.dbObj)
        otherPiece = otherSegment.piece()
        #if otherPiece.id < myId:
        #    continue
        otherPieceId = otherPiece.id
        if (otherPieceId is None):
            #print("   Skipping match for segment (%d): piece not found." % otherSegmentId)
            return (False, "PieceNotFound")
        foundSkip = False
        for pieceGroup in self.skipGroups:
            if myId in pieceGroup and otherPieceId in pieceGroup:
                foundSkip = True
                break
        if foundSkip is True:
            if otherPieceId not in skippedPieces:
                if self.printOutput:
                    print("   skipping all matches for (%d) %s: ratio %d" % 
                          (otherPiece.id, otherPiece.filename, ratioMatch.thisRatio))
                skippedPieces.append(otherPieceId)
            return (False, "SkipPiece")
        thisSegment = mysqlEM.Segment(ratioMatch.thisSegmentId, dbObj=self.dbObj)
        if (thisSegment.partId >= self.tenorPartNumber or 
                otherSegment.partId >= self.tenorOtherPartNumber):
            # tenor
            if ratioMatch.thisRatio - self.tenorThresholdAdd < self.minThreshold:
                return(False, "TenorBelowThreshold")
        return (True, (thisSegment, otherSegment, otherPiece))

    def checkOneMatch(self, p, ratioMatch, totalShown, skippedPieces):
        matches, info = self.checkForShow(p, ratioMatch, skippedPieces)
        if matches is False:
            return
        thisSegment, otherSegment, otherPiece = info
        totalShown += 1
        showInfo = "part %2d, m. %3d; (%4d) %30s, part %2d, m. %3d (ratio %5d)" % (
                                    thisSegment.partId, thisSegment.measureStart,
                                    otherPiece.id, otherPiece.filename, 
                                    otherSegment.partId, 
                                    otherSegment.measureStart, 
                                    ratioMatch.thisRatio)
    
        
        if totalShown > self.maxToShow:
            if otherPiece.id is not None: 
                # if segment matches but piece deleted... need to clean up orphen segments...
                print("   Not showing (too many matches): " + showInfo)
                return totalShown
        try:
            part = p.partFromSegmentPair(*ratioMatch)
        except TypeError:
            part = None
        if part is not None:
            print("   Showing -- " + showInfo)
            part.show()            
        else:
            if otherPiece.id is not None:
                print("  ERROR: not showing for lack of part: " + showInfo)
        return totalShown

if __name__ == '__main__':
    ss = SimilaritySearcher()
    ss.runPieces()
