# Generated by Django 4.0.5 on 2022-06-09 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emmsap2', '0009_intervals_intervals_one_char'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervals',
            name='piece',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emmsap2.piece'),
        ),
    ]