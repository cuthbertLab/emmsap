'''
Michael Tenzer asks: what's the highest and lowest note in the repertoire? 

July 25, 2016
'''
from emmsap import files
from music21 import pitch

# experimentally, these were found to have octave errors in some staff
incorrectlyEncoded = ['OMR', # do not trust OMR scores.
                      'OMF_PMFC14', # misspelled OMR
                      'FallowsMB_', # # 89 has a G5 but should not be in the dataset (much later)
                      'Chi_caval_msc', # octave error.
                      'Ciconia_Potential_Parody_Gloria',  # C2 is octave off
                      'E15cM-VII_BF-5_Excelsa_civitas_Vincentia', # mistake in CT m. 31
                      'E15cM_VII_Hubertus-1_Et_in_terra_Tro_Gloria_jubilatio.xml', 
                        # C1 mm 146-149 -- octave too high...
                      'London_29987_Antefana', # octave error
                      'Marchi_Notation_30-Gloria-Corona_Christi_lilia.xml', # hidden voice -- nope
                      'OscarV', # octave errors abound in Oscar's transcriptions
                      'PMFC_06_Jacopo_10-I_senti_ca_como', # octave error
                      'PMFC_06_Piero_03_Con_bracci_assai', # octave error (same transcriber)
                      'PMFC_07_GdF_9_La_Bella_E_La_Veccosa_Cavriola', # octave error
                      'PMFC_09_Bartolino_10-Inperial_sedendo', # octave error
                      'PMFC_07_VdR_3_Gridavan_Li_Pastor', # octave error
                      'PMFC_10_8-Deh_quanto_fa_gran_mal', # octave error
                      'PMFC_09_Bartolino_15-L_invido_per_lo_ben.xml', # octave error
                      'PMFC_10_Appendix_e-Plorans_ploravi(unfinished).xml', # octave error
                      'PMFC_10_Bonaiuto_3-Piata_ti_mova', # octave error
                      'PMFC_10_Stefani_2-I_senti_matutino.xml', # octave error IN PMFC
                      'PMFC_20_49-Jonesce_de_haut_corage', # octave error
                      # PMFC 44 is called PMFC 43 ! MISTAKE TO FIX!
                      'PMFC_22_50-Le_dieus_d_amours.xml', # octave error
                      'PMFC_24_34-O_rosa_bella.xml', # octave error
                      'PMFC_24_24-Regina_gloriosa.xml', # octave error in CT
                      'PMFC_24_41-Poy_che_morir.xml', # octave error
                      'Reggio_Emilia_Nella_Foresta.xml', # octave error
                      'PMFC_24_8-Gloria_Ciconia_8', # same as potential parody gloria
                      'Wolkenstein_Kom_liebster_man.capx', # octave error
                      ]

def main():
    fileIterator = files.FileIterator()
    #fileIterator.index = 0
    highestSoFar = pitch.Pitch('C3').ps
    lowestSoFar = pitch.Pitch('C5').ps
    
    for i,f in enumerate(fileIterator):
        if (i % 100) == 0 and i != 0:
            print("{} down!".format(i))
        skipIt = False
        for incorrect in incorrectlyEncoded:
            if incorrect in f.filePath:
                skipIt = True
                
        if skipIt:
            continue
        
        for n in f.recurse().notes:
            for p in n.pitches:
                if p.ps > highestSoFar:
                    highestSoFar = p.ps
                    print("New Highest Pitch {} in {} (m. {})".format(
                                                        p, f.filePath, n.measureNumber))
                elif p.ps == highestSoFar:
                    print("Tied Highest Pitch {} in {} (m. {})".format(
                                                        p, f.filePath, n.measureNumber))                    
                if p.ps < lowestSoFar:
                    lowestSoFar = p.ps
                    print("New Lowest Pitch {} in {} (m. {})".format(
                                                        p, f.filePath, n.measureNumber))
                elif p.ps == lowestSoFar:
                    print("Tied Lowest Pitch {} in {} (m. {})".format(
                                                        p, f.filePath, n.measureNumber))                    
                    
    print("Done...")

if __name__ == '__main__':
    main()