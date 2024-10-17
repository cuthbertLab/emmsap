# Generated by Django 5.1.1 on 2024-10-17 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emmsap2', '0012_alter_intervals_part_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composer',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='ratio',
            unique_together={('encoding_type', 'segment1', 'segment2')},
        ),
        migrations.AddIndex(
            model_name='ratio',
            index=models.Index(fields=['segment1'], name='emmsap2_rat_segment_7deaa9_idx'),
        ),
    ]
