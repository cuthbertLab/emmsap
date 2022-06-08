# Generated by Django 4.0.5 on 2022-06-07 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emmsap2', '0004_ratios_alter_segment_encoding_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ratios',
            new_name='Ratio',
        ),
        migrations.RemoveIndex(
            model_name='ratio',
            name='emmsap2_rat_encodin_24ad18_idx',
        ),
        migrations.AddIndex(
            model_name='ratio',
            index=models.Index(fields=['encoding_type'], name='emmsap2_rat_encodin_8c8985_idx'),
        ),
    ]
