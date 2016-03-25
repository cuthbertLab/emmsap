# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from __future__ import print_function, division

from emmsap import mysqlEM
#from music21.search import segment


skipPieces = [             
               # new discoveries!
               (2322, 2094), # PMFC Sanctus 16.55 + Autun 152 Modulus, Tenor Deo Gratias
               (2335, 1092, 908), # PMFC Ite Missa # 68 = PMFC 01 Tournai 6 - Ite Missa Est +
                             # Marchetto
               (2222, 2239), # Gloria 16.29 + 16.36
               (1242, 1610), # Franciscus L'adorno viso = PMFC 21.58 S'amours me het
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
                            # + Genitum non Factum. (just below threshold is Gloria 2 + Credo 3)
               # end new discoveries.
               
               # two transcriptions of the same
               # same piece..different versions.
               (2229, 1648), # Merci pour dieu A da Cividale E15c + PMFC22
               (2232, 717), # Je suy las venus E15c + Marchi notation
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
              (2274, 2275), # PMFC 16 #39, 40 -- different # of voices
              (2278, 2280), # PMFC 16,#43, 45 -- two credos related.
              
              
              # transpositions
              (1499, 1500), # Per un verde boschetto at two pitch levels.
              (1939, 1940), # Wolkenstein up a step.
              (1937, 1938), # Wolkenstein Mein herz, different pitches. Different meters.
              (1190, 1191), # Monophonic Credos in PMFC 23 at different pitch levels 
              (28, 1641, 1845), # Esperance and keyboard Asperance. + Santa Maria Maggiore
              
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
              (666, 82), # two transcriptions of PMFC04 14 Gli occhi
              
              
              (1530, 1531), 
              (1536, 1537),
              (1541, 1542, 638, 639), #ep 1541 later
              (1544, 1545, 1925),  # Je voy mon cuer, Du asserweltes schons
              (1550, 514), # 514 low match OMR gloria
              (1553, 1554),  # Mersi ou mort -- two versions
              
              (379, 2256), # Ciconia Gloria 8 + extract of the potential parody section...
              
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
              (281, 2240), # FOL, Grottaferrata Gloria in London Titus.
              (737, 1287), # Marchi and Di Mascia were right: 
                # Nuda non era is the best match for Le temps ver.
              (2125, 888), # FallowsMB_028_Min_herze_wil and PMFC 23.91 O_Quam_Pulchra_Puella ctrft
              (2093, 291), # Zachara, Fior Gentil and Gloria
              (1594, 1967), # PMFC 21_43 (Mais qu'il) Groeninghen Empris keyboard -- same up M2
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
              (168, 171, 397, 388, 807), # kyries based on Cunctipotens
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
              (852, 1190), # Credo village and a PMFC 23 Credo A1 -- monophonic rhythmic Credo 1.
              (1599, 1596), # IntRhySmall got that the Nightingale song of Or sus and 
                # Onques ne fu were the same. :-)
              
              
              
              # unknown similarities worth mentioning...
              (362, 1297), # Ciconia Io crido amor + Zaninus Se la lagrime -- m 16-17, 13-14
                # exact same sequential pattern that appears nowhere else.
              (1474, 1466), # PMFC 08 34 Pyance la bella iguana + PMFC 06 Giovanni 11a Nel meco
                    # m 42-57 and 17-31 both voices -- so similar in construction, argues that
                    # anonymous Pyance is by Giovanni. 
              (1802, 1365), # PMFC 11 58 mm. 13-18 identical to PMFC 11 17 -- m 15-20. 15 notes.
              (420, 1975), # Armes amours end = Se Zephirus ending
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
              
              (768, 939), # ends of PMFC_09_Paolo_30-Una_fera_gentil + 
                          # PMFC_07_GdF_2-Cacciand_Un_Giorno
                          # a little generic sounding, but rather similar...
              (1702, 2024), # Machaut Dame se vous m'estes mm. 6-10 = (identical)
                # Motet 14 De ma dolour 62-68 (one voice only...) 15 notes.
              (1840, 340), # Ciconia, O Padua 16-21, Albane 59-63. Very similar.
              
              
              
              # not false, but not necessarily worth mentioning
              (928, 769), # Not close enough, but DdF PMFC 07.16 + Paolo 9.31 Un pellegrin,
                # m24-29 to Paolo 19-25; different tactics to the same result.
              (1129, 1143), # PMFC10 no 24 + 10: m. 29-34 and 33-37 -- real similarities suggesting
                #same composer # HA! IN fact they are both by Andrea da Firenze. No wornder!
              
              
              # low threshold false matches
              (107, 202), # noodles in Italian music 
              (172, 1452), # noodles
              (148, 1768), # noodles
              (107, 1494), # noodles
              (107, 1449), # noodles
              (107, 1272), # noodles
              (1306, 1503), 
              (1476, 1116), 
              (1487, 1272), # noodles 
              (1775, 1064), # noodles
              (1240, 215),
              
              (1963, 388, 807, 169, 1488), # Machaut M3 and Ravenna Kyrie, + instrumental Faenza  
                # + Nicolo melisma
              (1365, 888), # Come Nfra I Altre Donne, O Quam Pulchra -- I wish, but not.
              (1962, 1474), # machaut M2 + PMFC 8-34 Pyance. No.
              (1967, 1236, 1641, 32, 815, 755, 1641), # Empris domoyres w/ much noodling.
              (1965, 370, 687, 1641, 386), # Machaut M6
              (687, 1705), # Is suo bel viso, Machaut B4
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
              (2338, 1655), # Jour a jour la vie -- PMFC 22.47a w/ Cristus PMFC.47b
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
              (211, 1271), # Piero All onbra + Paolo Girand un bel falcon.
              (939, 1271), # Cacciand Un Giorno + Paolo Girand
              (935, 1768), # DdF 7 + O tu chara scientia,
              (1349, 1487), # Bianchi Chi ama ending w/ Nicolo quando gli raggi...

              (2314, 2316), # PMFC 16 Sanctuses 47, 49 -- c.f. in 47 I = c.f. in 49 II
              (2315, 2322), # PMFC 16 Sanctuses 48, 55 -- same c.f.
              (2317, 2320, 2321, 2324), # PMFC 16 Sanctuses 50, 53, 54, 57 -- same c.f.
              (2319, 2008), # PMFC 16 Sanctuses 52, 02 -- c.f. salisbury 8.
              (2329, 2330, 2334), # PMFC 16 Agnus 62 and 63 (variants on each other) and c.f. for 67

            # IGNORE Tenors only...
            (276, 1338), # Gaudeamus Omnes + PMFC 08 Nicolo 24
            (2094, 166), # Autun 152 Deo Gratias + PMFC 12_44 Ave Verum Corpus -- not close enough
            (1982, 1163), # Turin 2b Patrem, PMFC 23.112 Gloria
            (1964, 32), # flos filius matches everything...
            (1080, 1097), # Barcelona Credo, Vitry Bona Condit
            (1083, 276), # Toulouse Kyrie, Gaudeamus Omnes
            (1084, 865), # Toulouse Sanctus, Credo Pellisson
            (1088, 480), # Tournai Gloria, Benedicamus Domino
            (2248, 1233), # Machaut Double hoquet, Degentis Vita tenor -- nope.
 
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
            (815, 934), # Keyboard Gloria + noodles
            (815, 172), # keyboard gloria + kyrie
            (1487, 152, 1349), 
            (107, 202), # Come da lupo, In verde prato.
            
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
            
            (286, 2119),
            (272, 782),
            (258, 1452),
            (255, 174),
            (187, 251),
            (243, 977), # Egidius Mille mercede Gentil aspetto -- maybe worth checking someday.
            (240, 1487),
            (234, 122),
            (224, 101),
            (220, 234),
            (217, 932),
            (215, 926),
            (211, 1467),
            (209, 1107),
            (207, 1767),
            (206, 1466),
            (204, 1280),
            (203, 1272),
            (202, 1964),
            (180, 1059),
            (174, 255),
            (172, 928),
            (171, 351),
            (170, 1967),
            (168, 1487),
            (165, 1229),
            (163, 165),
            (152, 1183),
            (150, 33),
            (149, 1467), 
            (147, 148),
            (146, 1064),
            (145, 927),
            (144, 1482),
            (142, 1771),
            (140, 146),
            (132, 1334),
            (128, 1107),
            (122, 234),
            (119, 932),
            (119, 1790),
            (116, 939),
            (107, 930),
            (102, 1494),
            (101, 1285),
            (100, 927),
            (99, 1467),
            (84, 1032),
            (77, 1681),
            (67, 1494),
            (64, 1291), # Sones ces Nachares and Cacciando per gustar; nice catch EMMSAP!
            (35, 1030), 
            (33, 994), # very francesco ending though...
            (9, 328),
            (1137, 101),
            (1116, 1487),
            (1129, 1320),
            (1114, 1105),
            (1111, 234),
            (1088, 1286),
            (1070, 1357),
            (1052, 1933),
            (1056, 979),
            (1054, 981),
            (1046, 1271),
            (101, 352),
            (187, 2015),
            (165, 1227),
            (286, 1463), # However, real evidence that Kyrie Summe Clementissime is Italian,
                # look at comparisons... All Italian cadences, mostly Francesco. Probably him.
            (399, 1483),
            (101, 352),
            (683, 994), 
            (107, 768),
            (807, 1469),
            (877, 1357),
            (970, 1467),
            (938, 1772),
            (107, 1116),
            (1183, 1272), # Credo Sorbonne, PMFC 08 15
            (1243, 1809), 
            (1281, 1487), 
            (1280, 1301),
            (1967, 1276),
            (148, 1271),
            (1281, 1267),
            (1243, 1809),
            (1268, 1281),
            (1314, 1316),
            (1344, 2210),
            (929, 1312),
            (897, 1452),
            (1468, 1768), # two Giovanni La Bella Stella O tu chara scientia -- very similar.
            (1486, 1770),
            (1414, 1418), # Mod 34, Mod 50 -- similar endings but nothing else.
            (1515, 1818),
            (1516, 1818), 
            (1593, 107), # 
            (1280, 1677),
            (931, 1789),
            (1779, 1767),
            (1776, 1280),
            (1770, 1771),
            (1272, 1767),
            (1183, 1944),
            (1487, 2013),
            (2, 1092),
            (14, 1218),
            (18, 485),
            (23, 1487),
            (29, 1963),
            (34, 1477),
            (38, 1365),
            (70, 1087),
            (67, 1452),
            (56, 1537),
            (55, 142),
            (53, 373),
            (50, 352),
            (49, 935),
            (49, 911),
            (102, 172),
            (99, 1770),
            (211, 1280),
            (319, 399),
            (350, 1507),
            (682, 1073),
            (702, 1451),
            (826, 1961),
            (374, 942),
            (983, 1009),
            (1017, 1024),
            (146, 1022),
            (886, 1770),
            (101, 927),
            (930, 1467),
            (152, 935),
            (984, 1142),
            (1010, 1032),
            (1072, 1768),
            (107, 1073),
            (211, 1101),
            (1141, 977),
            (122, 1284),
            (1322, 1772),
            (1337, 1356),
            (1354, 1488), 
            (207, 1446),
            (1046, 1480),
            (938, 1477),
            (1466, 1767),
            (207, 1473, 1446),
            (745, 1470),
            (1303, 1468),
            (1281, 1965),
            (1281, 1278),
            (1449, 1838),
            (1118, 1807),
            (306, 1779),
            (718, 2131),
            (1610, 2111), # Spesse fiate a preso PMFC 08.Anon39 m 5-11; PMFC 08.Nicolo16 I son 71-75
                # perfect, but not long enough to be a cite, but good evidence of Nicolo's
                # potential authorship? 
            (2062, 2067), # two polish MZR taht have really similar techniques 
                            # (Gloria + Credo; pair?)
            (211, 1770),
            (1480, 1312), #
            (33, 912), # De non fugir and lorenzo Di Riv a Riva -- 16 consecutive identical
                # pitches in a noodle. no quote or cite, but interesting for showing standard
                # techniques.
            (142, 1314), # Lorenzo Dolgomi Voi Maestri 19-21, Nicolo 18 It a veder ciascun 45-47
                # same noodle in sequence. 
            (215, 272), # Bartolino/Dactylus Inperial sedendo + Paolo Benedicamus noodles.
            
            (2231, 32), # Antonio da Cividale Pes + Flos Filius tenor
            (1983, 1984), # Turin masses OMR w/ cropped sections redone.
            (1995, 1829), # Turin mass tenor low match with PMFC 22.46
            (2008, 1096), # PMFC16 sanctus 2; low w/ Vitry Hugo Tenor
            (2009, 1965), # PMFC16 #3 Agnus; PMFC 2 SAmours tous amas joir. 
            (2015, 100), # kyrie PMFC 16 9 + melisma
            
            (2022, 1280), # machaut tenor + melismatic piece
            (2025, 1961), # two machaut tenors
            (2136, 1267), # FallowsMB_039_Quene_note.mxl PMFC8 Du_ancoliti
            
            (727, 731, 734, 736, 860, # hidden notes encoded in Marchi's transcriptions...
             170, 64, 176, 1291, 1563), # and pieces caught by them
              ] 

class SimilaritySearcher(object): # 1322
    def __init__(self, startPiece=2339, endPiece=2550, minThreshold=7500, maxToShow=0):
        self.dbObj = mysqlEM.EMMSAPMysql()
        self.startPiece = startPiece
        self.endPiece = endPiece
        self.minThreshold = minThreshold
        self.maxThreshold = 10001
        self.segmentType = 'DiaRhy2'
        #self.segmentType = 'IntRhySmall'
        self.skipGroups = skipPieces
        self.maxToShow = maxToShow
        self.skippedMatchPenalty = 0 # 300 # after skipping one, the odds of a good match goes down.
        self.tenorThresholdAdd = 500
        self.tenorPartNumber = 2
        self.tenorOtherPartNumber = 2
        self.printOutput = True
        self.fragmentsOnly = False
        
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
        if self.fragmentsOnly is True and p.frag is not True:
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
                                              segmentType=self.segmentType,
                                              maxThreshold=self.maxThreshold)
        return ratioMatches

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
        totalPenalty = len(skippedPieces) * self.skippedMatchPenalty
        if ratioMatch.thisRatio - totalPenalty < self.minThreshold:
            print("   below threshold for (%d) %s: ratio %d (adjusted to %d)" % 
                          (otherPiece.id, otherPiece.filename, 
                           ratioMatch.thisRatio, ratioMatch.thisRatio - totalPenalty))
            skippedPieces.append(otherPieceId)
            return(False, "TooCommonPenaltyThreshold")
        
        return (True, (thisSegment, otherSegment, otherPiece))


if __name__ == '__main__':
    ss = SimilaritySearcher()
    ss.runPieces()
