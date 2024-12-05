# -*- coding: utf-8 -*-
#----------------------------------
'''
Populates the MYSQL database using info from the directory and sheets

Run updateDB instead of this before searching via similarityDB
'''
from django.core.management.base import BaseCommand  # , CommandError


from ...models import Piece
from ...files import allFiles
from ...index_segments import main as index_segments_main
from ...index_ratios import update_ratio_table_parallel
from ...index_texts import main as index_texts_main
from ...index_tinyNotation import main as index_tinyNotation_main


class Command(BaseCommand):
    help = 'Index files from the disk'

    def handle(self, *args, **options):
        '''
        Tasks when the database is updated
        '''
        self.updateFiles()
        index_texts_main()
        index_tinyNotation_main()
        index_segments_main('dia_rhy')
        index_segments_main('int_dia_diff')
        update_ratio_table_parallel('dia_rhy')
        update_ratio_table_parallel('int_dia_diff')
        print('Done!')

    def updateFiles(self):
        all_files = allFiles()
        filenames = Piece.objects.all().values_list('filename', flat=True)
        # print(list(zip(sorted(all_files), sorted(filenames))))
        # exit(0)

        out = []
        for disk_file in all_files:
            if disk_file not in filenames:
                print(disk_file)
                new_piece = Piece(filename=disk_file)
                new_piece.save()
                out.append((new_piece.id, new_piece.filename))

        for piece_id, piece_filename in out:
            print(f'{piece_id} {piece_filename}')
        print(f'Added {len(out)} files.')

