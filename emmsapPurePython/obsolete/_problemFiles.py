# for bugtesting problem files...
from emmsap import files

emDir = files.emmsapBase
problems = [
            'PMFC_12_7-Gloria_Engardus.xml',
            'PMFC_12_4-Gloria_Rvat_1419.xml',
            #'PMFC_06_Piero_1-All_onbra_d_un_perlato.xml',
            'PMFC_04-A_lle__s_andra_lo_spirt_.xml',
            #'Marchi_Notation_7b-conbien_que_lontain_suj_de_vous_dame_chiere.xml',
            #'Marchi_Notation_7a-conbien_que_lontain_suj_de_vous_dame_chiere.xml',
            #'Marchi_Notation_6-Jaym_la_plus_belle_jaime_la_plus_souveraine.xml',
            #'Marchi_Notation_36-Gloria-O_felix_certe_civitas_urbeventana_gaude.xml',
            ]
from music21 import converter

for x in problems:
    fn = emDir + x
    try:
        c = converter.parse(fn, forceSource=True)
        print(c)
        #c.show()
    except Exception as e:
        print(e)
        print(x)
        #exit()
        
        